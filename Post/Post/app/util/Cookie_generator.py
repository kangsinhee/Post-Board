from Post.config.app_config import DevLevelAppconfig
from Post.app.util.Token_generator import generate_access_token, generate_refresh_token, decode_token

class generate_cookie():
    def __init__(self, resp):
        self.resp = resp

    def access_cookie(self, Userid, nickname):
        self.resp.set_cookie("Access_Token", generate_access_token(Userid, nickname),
                        max_age=DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME, Secure = True)

    def refresh_cookie(self, Userid, nickname):
        self.resp.set_cookie("Refresh_Token", generate_refresh_token(Userid, nickname),
                        max_age=DevLevelAppconfig.REFRESH_TOKEN_EXPIRE_TIME, Secure = True)

    def delete_cookie(self):
        self.resp.set_cookie("Access_Token", '', max_age=0)
        self.resp.set_cookie("Refresh_Token", '', max_age=0)
