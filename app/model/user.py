import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask import current_app
from .. import db #, login_manager


class Permission:
    API_ACCESS = 0x01
    WEB_ACCESS = 0x02
    ADMINISTATOR = 0x80


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    secret = db.Column(db.String(128))
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def can(self, permission):
        return (self.permissions & permission) == permission


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

#login_manager.anonymous_user = AnonymousUser


#@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
