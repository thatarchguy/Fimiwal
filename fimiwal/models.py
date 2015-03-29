from fimiwal import db
import datetime


class Clients(db.Model):
    """
    Database Model for Clients
    """
    id          = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(64), index=True, unique=True)
    date_added  = db.Column(db.String(20))
    key         = db.Column(db.String(256))
    ip          = db.Column(db.String(20))
    active      = db.Column(db.Boolean, unique=False, default=True)
    date_rm     = db.Column(db.String(20))

    def __repr__(self):
        return '<Name %r>' % (self.name)




class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username    = db.Column('username', db.String(20), unique=True, index=True)
    password    = db.Column('password', db.String(40))
    email       = db.Column('email', db.String(50), unique=True, index=True)

    def __init__(self, username, password, email):
        self.username   = username
        self.password   = password
        self.email      = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)
