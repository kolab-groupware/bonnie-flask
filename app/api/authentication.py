from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from functools import wraps
from errors import unauthorized, forbidden
from ..model import User, Permission, AnonymousUser
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(username = username).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

