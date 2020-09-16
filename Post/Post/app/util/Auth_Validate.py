from functools import wraps
from flask import request, make_response, redirect, url_for, session

from Post.app.exception import AuthenticateFailed
from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie
from Post.app.models import User

def Auth_Validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            Access_Token = Check_Token(Token_name="Access_Token")
        except:
            Extend_Token = Extend_access_Token()

            return Extend_Token
        return f(*args, **kwargs)
    return wrapper

def Check_Token(Token_name):
    cookie = request.cookies.get(Token_name)
    Token = decode_token(cookie)
    return Token

def Extend_access_Token():
    try:
        Token = Check_Token(Token_name="Refresh_Token")
        if Token is not None:
            resp = make_response(redirect())
            Cookie = generate_cookie(resp)
            Cookie.access_cookie(Token["sub"], Token["nickname"])

            return resp
        else:
            raise AuthenticateFailed()
    except:
        raise AuthenticateFailed()