import os
import datetime
from datetime import timedelta


class DefaultAppConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = ""

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER_LOCATION")
    ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=5)
    REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days=14)

class DevLevelAppconfig(DefaultAppConfig):
    SECRET_KEY = os.getenv("SECRET_KET")
