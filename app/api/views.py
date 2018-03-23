from flask import request, jsonify, make_response
from . import api
from ..models import User
from .errors import unauthorized, forbidden, bad_request

DEFAULT_EXPIRATION = 3600 * 24

@api.route('/login', methods=['POST'])
def login():
    """
    以下情况会出现 `invalid request` 错误：
    1. data 不是 json 格式
    2. username 不存在
    3. password 不存在

    以下情况会出现 `invalid data type` 错误：
    1. days 的值不是 int 类型

    以下情况会出现 `invalid data value` 错误：
    1. days 的值不是 7

    以下情况会出现 `invalid username` 错误：
    1. 用户名 username 不存在

    """
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return bad_request('invalid request')
    username = request.json['username']
    password = request.json['password']
    if 'days' in request.json :
        days = request.json['days']
        if not isinstance(days, int):
            return bad_request('invalid data type')
        elif days != 7:
            return bad_request('invalid data value')
        else:
            expiration = 7 * DEFAULT_EXPIRATION
    else:
        expiration = DEFAULT_EXPIRATION

    user = User.objects(username=username).first()
    if not user:
        return bad_request('invalid username')
    if user is not None and user.verify_password(password):
        token = user.generate_api_token(expiration=expiration)
        if len(user['tokens']) < 3:
            user['tokens'].append(token)
            user.save()
            return jsonify({'token': token, 'expiration': expiration,
                        'message':'success',"username":username}), 200
        else:
            return forbidden('login limted')
    return bad_request('invalid password')

@api.route('/register', methods=['POST'])
def register():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return bad_request('invalid request')
    username = request.json['username']
    password = request.json['password']
    user = User.objects(username=username).first()
    if user:
        return bad_request('username already used')
    user = User(username=username,password=password)
    user.save()
    return jsonify({'message': "success", 'username':user['username']}), 200

def verify_token(token):
    user = User.objects(tokens__contains=token).first()
    if not user:
        return False
    if User.verify_api_token(token):
        return True
    user['tokens'].remove(token)
    user.save()
    return False

@api.route('/info',methods=['POST'])
def info():
    if not request.json or not 'token' in request.json:
        return bad_request('invalid request')
    if not verify_token(request.json['token']):
        return bad_request('invalid token')
    user = User.objects(tokens__contains=request.json['token']).first()
    return jsonify(user.to_json()), 200


@api.route('/update/age',methods=['POST'])
def update_age():
    if not request.json or not 'age' in request.json or not 'token' in request.json:
        return bad_request('invalid request')
    if not verify_token(request.json['token']):
        return bad_request('invalid token')
    age = request.json['age']
    if not isinstance(age, int):
        return bad_request('invalid data type')
    elif age > 100 or age < 0:
        return bad_request('invalid data value')
    user = User.objects(tokens__contains=request.json['token']).first()
    if user:
        user['age'] = age
        user.save()
    return jsonify({'message': 'success', 'age': age}), 200


@api.route('/logout',methods=['POST'])
def logout():
    if not request.json or not 'token' in request.json:
        return bad_request('invalid request')
    if not verify_token(request.json['token']):
        return bad_request('invalid token')
    user = User.objects(tokens__contains=request.json['token']).first()
    user['tokens'].remove(request.json['token'])
    user.save()
    return jsonify({'message': 'success','username':user['username'] }), 200
