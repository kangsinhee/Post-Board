from Post.app.extension import db

class Ben_list(db.Model):
    __tablename__ = "ben_list"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    uuid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return "< BEN id = %s >" % (self.id)