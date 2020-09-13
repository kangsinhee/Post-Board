import jwt
import time

from Post.config.app_config import DevLevelAppconfig
from Post.app.exception import AuthenticateFailed

def generate_token(Userid, token_type, expire_time):
    payload = {
        "iat" : int(time.time()),
        "sub" : Userid,
        "type" : token_type
    }
    return jwt.encode(payload, DevLevelAppconfig.SECRET_KEY, algorithm="HS256")

def generate_access_token(Userid):
    token = generate_token(
        Userid, "access_token", DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME
    )
    return token.decode()

def generate_refresh_token(Userid):
    token = generate_token(
        Userid, "refresh_token", DevLevelAppconfig.REFRESH_TOKEN_EXPIRE_TIME
    )
    return token.decode()

def decode_token(token):
    return jwt.decode(token, DevLevelAppconfig.SECRET_KEY, verify=False)["sub"]