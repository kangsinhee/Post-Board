from Post.config.app_config import DevLevelAppconfig
from Post.app.util.Token_generator import generate_access_token, generate_refresh_token, decode_token

class generate_cookie():
    def __init__(self, resp):
        self.resp = resp

    def access_cookie(self, User):
        self.resp.set_cookie("Access_Token", generate_access_token(User),
                        max_age=DevLevelAppconfig.ACCESS_TOKEN_EXPIRE_TIME)

    def refresh_cookie(self, User):
        self.resp.set_cookie("Refresh_Token", generate_refresh_token(User),
                        max_age=DevLevelAppconfig.REFRESH_TOKEN_EXPIRE_TIME)

    def delete_cookie(self):
        self.resp.set_cookie("Access_Token", '', max_age=0)
        self.resp.set_cookie("Refresh_Token", '', max_age=0)
