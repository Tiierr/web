from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
from mongoengine import *
from flask_mongoengine import BaseQuerySet


class User(UserMixin, DynamicDocument):
    meta = {
        'collection': 'users',
        'strict': False,
        'queryset_class': BaseQuerySet
    }
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    age = IntField(required=True, default=18)
    sex = StringField(required=True, default='male')
    tokens =  ListField(default=[])

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def verify_api_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.objects(username=data['username']).first()

    def generate_api_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'username': self.username}).decode('ascii')

    def to_json(self):
        json_user = {
            'username': self.username,
            'age': self.age,
            'sex': self.sex
        }
        return json_user
