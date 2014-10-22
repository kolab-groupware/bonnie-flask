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

import json
import logging
from flask import Blueprint, current_app, request
from flask.ext.login import login_required, current_user

from app import db
from app.auth import auth, permission_required
from app.model import User, Permission

data = Blueprint('data', __name__, url_prefix='/data')
log = logging.getLogger('data')

def jsonify(data):
    """
        Similar to flask.jsonify but simply dumps the single argument as JSON
    """
    return current_app.response_class(json.dumps(data, indent=None if request.is_xhr else 2),
        mimetype='application/json')

def abort(errcode, errmsg):
    response = jsonify({ 'error': errmsg })
    response.status_code = errcode
    return response

def notfound():
    return abort(404, 'Not Found')


@data.route('/users', methods=['GET','POST'])
@login_required
@permission_required(Permission.ADMINISTATOR)
def users():
    result = []

    # respond to GET request
    if request.method == 'GET':
        for user in User.query.all():
            result.append(user.to_json())

    elif request.method == 'POST':
        save_data = request.get_json(True, True)
        save_data.pop('password-check', None)

        try:
            user = User(**save_data)
            if user.validate():
                db.session.add(user)
                db.session.commit()
                result = { 'success': True, 'id': user.id }
            else:
                return abort(500, 'Validation error: ' + '; '.join(user.validation_errors))

        except Exception, e:
            log.error("Error creating user: %r; DATA=%r", e, save_data)
            return abort(500, 'Saving error')

    return jsonify(result)


@data.route('/users/<id>', methods=['GET','PUT','DELETE'])
@login_required
@permission_required(Permission.ADMINISTATOR)
def users_rec(id):
    result = {}

    user = db.session.query(User).get(id)
    if user is None:
        return notfound()

    # respond to GET request
    if request.method == 'GET':
        result = user.to_json()
        # flag current user
        if user.id == current_user.id:
            result['_isme'] = True

    # handle updates from PUT requests
    elif request.method == 'PUT':
        save_data = request.get_json(True, True)
        save_data.pop('password-check', None)

        # don't allow one to change its own permissions
        if user.id == current_user.id:
            save_data.pop('permissions', None)

        try:
            user.update(save_data)

            if user.validate():
                db.session.add(user)
                db.session.commit()
                result = { 'success': True }
            else:
                return abort(500, 'Validation error; ' + '; '.join(user.validation_errors))

        except Exception, e:
            log.error("Error saving user: %r; DATA=%r", e, save_data)
            return abort(500, 'Saving error')

    # handle DELETE requests
    elif request.method == 'DELETE':
        if user.id == current_user.id:
            log.warning("User tried to delete itself")
            return abort(403, 'Operation not permitted')

        try:
            db.session.delete(user)
            db.session.commit()
            result = { 'success': True }
        except Exception, e:
            log.error("Error deleting user: %r", e)
            return abort(500, 'Delete error')

    return jsonify(result)
