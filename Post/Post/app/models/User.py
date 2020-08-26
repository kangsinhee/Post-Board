from Post.app import db, jwt
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'mysql_collate' : 'utf8_general_ci'}
    Userid = db.Column(db.String(30), nullable=False, primary_key=True, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(45), nullable=False, unique=True)

    def __init__(self, Userid, password, nickname):
        self.Userid = Userid
        self.nickname = nickname
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)