import jwt

from functools import wraps
from flask import request

from Post.config.app_config import DevLevelAppconfig
from Post.app.exception import AuthenticateFailed, Unauthorized
from Post.app.util.token_generator import decode_token

def token_checker(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers["Authorization"][7:]
        if token is not None:
            try:
                payload = jwt.decode(token, DevLevelAppconfig.SECRET_KEY, "HS256")["sub"]
            except:
                payload = None
                raise AuthenticateFailed
        else:
            raise AuthenticateFailed
        return f(*args, **kwargs)
    return wrapper
