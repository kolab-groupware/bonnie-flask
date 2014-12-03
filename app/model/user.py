# -*- coding: utf-8 -*-
#
# Copyright 2014 Kolab Systems AG (http://www.kolabsys.com)
#
# Thomas Bruederli <bruederli at kolabsys.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import hashlib
from sqlalchemy import not_
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask.ext.babel import gettext as _
from flask import current_app
from .. import db, login_manager


class Permission:
    API_ACCESS = 0x01
    WEB_ACCESS = 0x02
    ADMINISTRATOR = 0x80


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
        self.validation_errors = []

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

    def update(self, attrib):
        for key, value in attrib.iteritems():
            if not key == 'id' and hasattr(self, key):
                setattr(self, key, value)

        if attrib.has_key('password'):
            self.password = attrib['password']

    def validate(self):
        self.validation_errors = []

        if self.username.strip() == '':
            self.validation_errors.append(_("Username must not be empty"))
        elif User.query.filter(User.username==self.username, not_(User.id==self.id)).count() > 0:
            self.validation_errors.append(_("Username already taken"))

        return len(self.validation_errors) == 0

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'permissions': self.permissions,
            'secret': self.secret,
        }


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
