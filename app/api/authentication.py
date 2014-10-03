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

import hmac
import hashlib
from flask import g, request, current_app
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
    """
        Permission check decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kw):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kw)
        return decorated_function
    return decorator


def signature_required():
    """
        Request signature verification decorator
    """
    def decorator(f):
        def decorated_function(*args, **kw):
            if not verify_request(request):
                return forbidden('Invalid Request Signature')
            return f(*args, **kw)
        return decorated_function
    return decorator


def verify_request(request):
    # check for allowed source IP
    allowed_ips = current_app.config['API'].get('allow', '').split(',')
    if request.remote_addr in allowed_ips:
        return True

    user = g.current_user
    signature = request.headers.get('X-Request-Sign', None)
    if not user or signature is None:
        return False

    sign = hmac.new(
        key=user.secret.encode('utf8'),
        msg=request.headers.get('X-Request-User') + ':' + request.data,
        digestmod=hashlib.sha256
    ).hexdigest()

    return signature == sign
