import os
import datetime
from werkzeug.utils import secure_filename

class DefaultAppConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = ""

    UPLOAD_FOLDER = "/Post-Board/Post/Post/upload/"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days=14)

class DevLevelAppconfig(DefaultAppConfig):
    SECRET_KEY = os.getenv("SECRET_KET")

def allowed_file(filename):
    return '.' in filename and \
        filename.replit('.', 1)[1].lower() in DevLevelAppconfig.ALLOWED_EXTENDIONS