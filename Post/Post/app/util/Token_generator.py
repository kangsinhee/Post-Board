import jwt
import time

from Post.config.app_config import DevLevelAppconfig
from Post.app.exception import AuthenticateFailed

def generate_token(token_type, Userid, nickname, expire_time):
    payload = {
        "iat" : int(time.time()),
        "exp" : int(time.time() + expire_time),
        "Userid" : Userid,
        "nickname" : nickname,
        "type" : token_type
    }
    return jwt.encode(payload, DevLevelAppconfig.SECRET_KEY, algorithm="HS256")

def generate_access_token(Userid, nickname):
    token = generate_token(
        "access_token", Userid, nickname, DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME
    )
    return token.decode()

def generate_refresh_token(Userid, nickname):
    token = generate_token(
        "refresh_token", Userid, nickname, DevLevelAppconfig.REFRESH_TOKEN_EXPIRE_TIME
    )
    return token.decode()

def decode_token(token):
    return jwt.decode(token, DevLevelAppconfig.SECRET_KEY, verify=False)["Userid"]

def decode_token(token, name):
    return jwt.decode(token, DevLevelAppconfig.SECRET_KEY, verify=False)[name]