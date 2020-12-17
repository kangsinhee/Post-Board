from flask import Flask
from Post.app.view import Blueprint

def create_app(*config_cls) -> Flask:
    app = Flask(__name__)
    for config in config_cls:
        app.config.from_object(config)
        app.register_blueprint(Blueprint)
    return app

from Post.app import view
from Post.app import models