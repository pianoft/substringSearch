# flask_blog/models/entries.py
from flask_blog import db
from datetime import datetime  # これはモデュール


class Entry(db.Model):
    __tablename__ = 'entries'
    # primarykeyはユニークではないといけない
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    body = db.Column(db.String(30))
    stat = db.Column(db.Boolean)
    cnt = db.Column(db.Integer)

    def __init__(self, title=None, text=None, body=None, stat=None, cnt=None):
        self.title = title
        self.text = text
        self.body = body
        self.stat = stat
        self.cnt = cnt
        self.created_at = datetime.utcnow()
