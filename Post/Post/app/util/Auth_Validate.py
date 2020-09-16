from flask import request, make_response, session, redirect, url_for
from Post.app.exception import AuthenticateFailed

from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie
from functools import wraps

def Auth_Validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            Access_token = decode_token_in_cookie("Access_Token")
        except:
            resp = Extend_Access_token()
            return resp
        return f(*args, **kwargs)
    return wrapper

def decode_token_in_cookie(token):
    cookie = request.cookies.get(token)
    token = decode_token(cookie)
    return token

def Extend_Access_token():
    try:
        Refresh_Token = decode_token_in_cookie("Refresh_Token")
        if Refresh_Token != None:
            resp = make_response()
            Cookie = generate_cookie(resp)
            Cookie.access_cookie(Userid=Refresh_Token, nickname="nickname")

            return resp
        else:
            raise AuthenticateFailed()
    except:
        print("extend error")