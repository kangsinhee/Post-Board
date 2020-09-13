import jwt

from functools import wraps
from flask import request, make_response, redirect, url_for

from Post.config.app_config import DevLevelAppconfig
from Post.app.exception import AuthenticateFailed, Unauthorized
from Post.app.util.Token_generator import decode_token

def Auth_Validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            Access_cookie = request.cookies.get("Access_Token")
            Access_Token = decode_token(Access_cookie)
        except:
            resp = make_response(redirect(url_for('index')))
            raise AuthenticateFailed()

        print(Access_Token)
        return f(*args, **kwargs)
    return wrapper
