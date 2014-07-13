from approot import db

from .common import TimestampMixin


class User(db.Model, TimestampMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)

    # Relations
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User(name={}, user_id={})>'.format(self.username, self.user_id)
