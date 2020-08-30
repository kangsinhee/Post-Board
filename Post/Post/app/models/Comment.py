from Post.app.extension import db

class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    uuid = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.uuid'), nullable=False)
    nickname = db.Column(db.String(45), nullable=False)
    content = db.Column(db.Text(1000), nullable=False)
    create_time = db.Column(db.DateTime(), nullable=False)

    def __init__(self, post_id, nickname, content, create_time):
        self.post_id = post_id
        self.nickname = nickname
        self.content = content
        self.create_time = create_time

    def __repr__(self):
        return "< uuid = %s, post_id = %s, writer = %s >" % (self.uuid, self.post_id, self.nickname)