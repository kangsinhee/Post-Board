from flask import request, make_response
from Post.app.exception import AuthenticateFailed

from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie
from functools import wraps

def Auth_Validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            decode_cookie_in_token("Access_Token", "Userid")
        except:
            resp = Extend_Access_token()
            return resp
        return f(*args, **kwargs)
    return wrapper

def decode_cookie_in_token(type, payload):
    try:
        cookie = request.cookies.get(type)
        token = decode_token(cookie, payload)
        return token
    except:
        raise AuthenticateFailed()

def Extend_Access_token():
    try:
        Refresh_Token = decode_cookie_in_token("Refresh_Token", "Userid")
        if Refresh_Token != None:
            resp = make_response()
            Cookie = generate_cookie(resp)
            Cookie.access_cookie(Refresh_Token)

            return resp
    except:
        raise AuthenticateFailed()