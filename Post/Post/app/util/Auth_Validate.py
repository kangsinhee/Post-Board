from functools import wraps
from flask import request, make_response, redirect, url_for

from Post.app.exception import AuthenticateFailed
from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie

def Auth_Validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            Load_Token(Token_name="Access_Token")
        except:
            return Extend_access_Token()
        return func(*args, **kwargs)
    return wrapper

def Load_Token(Token_name):
    try:
        cookie = request.cookies.get(Token_name)
        Token = decode_token(cookie)
    except:
        Token = None
    return Token

def Extend_access_Token():
    try:
        Token = Load_Token(Token_name="Refresh_Token")
        if Token is not None:
            resp = make_response(redirect(request.url))
            Cookie = generate_cookie(resp)
            Cookie.access_cookie(Token["userid"], Token["nickname"])
            return resp
        else:
            raise AuthenticateFailed()
    except:
        raise AuthenticateFailed()