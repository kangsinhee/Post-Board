from Post.app import db

class Post(db.Model):
    __tablename__ = "post"
    __table_args__ = {'mysql_collate' : 'utf8_general_ci'}
    uuid = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, nullable=True)

    writer = db.Column(db.String(45), db.ForeignKey('user.nickname'), default='(알수없음)')

    def __init__(self, title, content, created_at, writer):
        self.title = title
        self.content = content
        self.created_at = created_at
        self.writer = writer