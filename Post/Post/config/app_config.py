import os

class DefaultAppConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = ""
    JWT_SECRET_KEY = ""

class DevLevelAppconfig(DefaultAppConfig):
    SECRET_KEY = "default-secretkey"
    JWT_SECRET_KEY = "jwt-secretkey"