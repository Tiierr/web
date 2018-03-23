from flask import jsonify, make_response
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

@api.app_errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'bad request', 'code':'400'}), 400)

@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found', 'code':'404'}), 404)

@api.app_errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'internal server error', 'code':'500'}), 500)
