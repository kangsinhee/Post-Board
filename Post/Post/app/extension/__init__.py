from Post.app import create_app
from flask_sqlalchemy import SQLAlchemy

from Post.config.db_config import LocalDBConfig
from Post.config.app_config import DevLevelAppconfig

app = create_app(LocalDBConfig, DevLevelAppconfig)
db = SQLAlchemy(app)