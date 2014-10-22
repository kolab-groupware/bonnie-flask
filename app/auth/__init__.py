from flask import Blueprint
from functools import wraps
from flask import abort
from flask.ext.login import current_user

auth = Blueprint('auth', __name__)

from . import views

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kw):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kw)
        return decorated_function
    return decorator
