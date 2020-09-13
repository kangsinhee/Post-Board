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
            Access_cookie = request.cookies.get("Access_Token")
            Access_Token = decode_token(Access_cookie)
        except:
            Refresh_cookie = request.cookies.get("Refresh_Token")
            Refresh_Token = decode_token(Refresh_cookie)
            if Refresh_Token is not None:
                user = session.get('User', None)
                user_info = User.query.filter_by(nickname = user).first()

                resp = make_response(redirect(url_for('index')))
                Cookie = generate_cookie(resp)
                Cookie.access_cookie(user_info.Userid)

                return resp
            else:
                raise AuthenticateFailed()

        print(Access_Token)
        return f(*args, **kwargs)
    return wrapper
