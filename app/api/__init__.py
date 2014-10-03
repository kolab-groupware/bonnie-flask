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

from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

from . import authentication, errors, rpc
from authentication import signature_required

auth = authentication.auth


@api.before_request
def before_request():
    api.input = dict()
    request.env = dict()

    if request.method == 'POST':
        api.input.update(request.get_json(True, True))
        rpc.reqid = api.input['id'] if api.input.has_key('id') else None

    # TODO: check X-Request-User and resolve to nsuniqueid ?
    request.env['REQUEST_USER'] = request.headers.get('X-Request-User')
    request.env['REMOTE_ADDR'] = request.remote_addr


@api.route('/')
def index():
    return jsonify(dict(error="Invalid Request")), 400


@api.route('/env', methods=['GET','POST'])
def env():
    return jsonify(dict(
        METHOD=request.method,
        GET=request.args,
        DATA=api.input,
        ENV=request.env,
        Headers=[(k,request.headers.get(k)) for k in request.headers.keys()]
    ))


@api.route('/<cmd>', methods=['POST'])
@auth.login_required
@signature_required()
def _default(cmd):
    # TODO: implement the REST API for requests like /api/<model.method>
    return jsonify(dict(command=cmd))
