from flask import Flask
from flask_mongoengine import MongoEngine
from flask_session import Session
from config import config

db = MongoEngine()
ss = Session()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ss.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
