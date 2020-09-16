from Post.config.app_config import DevLevelAppconfig
from Post.app.util.Token_generator import generate_token

class generate_cookie():
    def __init__(self, resp):
        self.resp = resp

    def generate_all_cookies(self, Userid, nickname):
        self.access_cookie(Userid, nickname)
        self.refresh_cookie(Userid, nickname)

    def access_cookie(self, Userid, nickname):
        self.resp.set_cookie("Access_Token", generate_token("Access_Token", Userid, nickname),
                        max_age=DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME)

    def refresh_cookie(self, Userid, nickname):
        self.resp.set_cookie("Refresh_Token", generate_token("Refresh_Token", Userid, nickname),
                        max_age=DevLevelAppconfig.REFRESH_TOKEN_EXPIRE_TIME)

    def delete_cookie(self):
        self.resp.set_cookie("Access_Token", '', max_age=0)
        self.resp.set_cookie("Refresh_Token", '', max_age=0)
