from Post.app.extension import db

class Files(db.Model):
    __tablename__ = "files"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    Userid = db.Column(db.String(30), nullable=False, primary_key=True)
    file_adr = db.Column(db.String(150), nullable=False)

    def __init__(self, Userid, file_adr):
        self.Userid = Userid
        self.file_adr = file_adr