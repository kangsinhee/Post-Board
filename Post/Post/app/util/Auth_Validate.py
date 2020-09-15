from flask import request, make_response, redirect, url_for, session
from Post.app.exception import AuthenticateFailed

from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie
from functools import wraps

def Auth_Validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            check_Access_token()
        except:
            resp = extend_Access_token()
            return resp
        return f(*args, **kwargs)
    return wrapper

def check_Access_token():
    try:
        cookie = request.cookies.get("Access_Token")
        Access_Token = decode_token(cookie)

        return Access_Token
    except:
        raise AuthenticateFailed()

def check_Refresh_token():
    try:
        cookie = request.cookies.get("Refresh_Token")
        Refresh_Token = decode_token(cookie)

        return Refresh_Token
    except:
        raise AuthenticateFailed()

def extend_Access_token():
    try:
        Refresh_Token = check_Refresh_token()
        if Refresh_Token != None:
            resp = make_response()
            Cookie = generate_cookie(resp)
            Cookie.access_cookie(Refresh_Token)

            return resp
    except:
        raise AuthenticateFailed()