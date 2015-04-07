from fimiwal import db
import datetime


class Clients(db.Model):
    """
    Database Model for Clients
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    date_added = db.Column(db.String(20))
    ident = db.Column(db.String(50))
    ip = db.Column(db.String(20))
    os = db.Column(db.String(20))
    directory = db.Column(db.String(255))
    ssh = db.Column(db.String(1024))
    scans = db.relationship('Scans', backref='client', lazy='dynamic')
    active = db.Column(db.Boolean, unique=False, default=True)
    date_rm = db.Column(db.String(20))

    def __repr__(self):
        return '<Email %r>' % (self.email)


class Scans(db.Model):
    """
    Database Model for Scans ran
    """
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    date = db.Column(db.String(20))
    status = db.Column(db.String(10))
    diff = db.Column(db.Text())

    def __repr__(self):
        return '<Date %r>' % (self.date)


class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(40))
    email = db.Column('email', db.String(50), unique=True, index=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

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
