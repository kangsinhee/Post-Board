from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
def create_app(*config_cls) -> Flask:
    app = Flask(__name__)
    for config in config_cls:
        app.config.from_object(config)
    return app

from Post.config.db_config import LocalDBConfig
from Post.config.app_config import DevLevelAppconfig

app = create_app(LocalDBConfig, DevLevelAppconfig)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from Post.app.view import Post, User_Account
from Post.app.models import Post, User