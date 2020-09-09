import os
import datetime

class DefaultAppConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = ""
    JWT_SECRET_KEY = ""

    JWT_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True

class DevLevelAppconfig(DefaultAppConfig):
    SECRET_KEY = "default-secretkey"
    JWT_SECRET_KEY = "jwt-secretkey"

