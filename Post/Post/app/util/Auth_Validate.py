from functools import wraps
from flask import request, make_response, redirect, url_for

from Post.app.exception import AuthenticateFailed
from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import Manage_cookie

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
    cookie = request.cookies.get(Token_name)
    Token = decode_token(cookie)

    return Token

def Extend_access_Token():
    try:
        Token = Load_Token(Token_name="Refresh_Token")
        if Token != None:
            resp = make_response(redirect(request.url))
            Cookie = Manage_cookie(resp)
            Cookie.access_cookie(Token["userid"], Token["nickname"])
            return resp
    except:
        raise AuthenticateFailed()