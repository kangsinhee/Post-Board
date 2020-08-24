import os
import datetime

class DefaultAppConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = ""
    JWT_SECRET_KEY = ""
    ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=5)
    REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days=7)

class DevLevelAppconfig(DefaultAppConfig):
    SECRET_KEY = "default-secretkey"
    JWT_SECRET_KEY = "jwt-secretkey"