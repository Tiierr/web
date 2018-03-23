import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyM'
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')
    MONGODB_SETTINGS = {
                        'db': 'user',
                        'host': 'localhost',
                        'port': 27017
                       }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
