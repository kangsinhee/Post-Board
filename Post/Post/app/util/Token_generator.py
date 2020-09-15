import jwt
import time

from Post.config.app_config import DevLevelAppconfig

def default_generate_token(token_type, Userid, nickname, expire_time):
    payload = {
        "iat" : int(time.time()),
        "exp" : int(time.time()) + int(expire_time.seconds),
        "Userid" : Userid,
        "nickname" : nickname,
        "type" : token_type
    }
    return jwt.encode(payload, DevLevelAppconfig.SECRET_KEY, algorithm="HS256")

def generate_token(type, Userid, nickname):
    token = default_generate_token(
        type, Userid, nickname, DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME
    )
    return token.decode()

def decode_token(type, payload):
    return jwt.decode(type, DevLevelAppconfig.SECRET_KEY, verify=False)[payload]