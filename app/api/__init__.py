from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

from . import authentication, errors, rpc
auth = authentication.auth


@api.before_request
def before_request():
    api.input = dict()
    request.env = dict()

    if request.method == 'POST':
        api.input.update(request.get_json(True, True))
        rpc.reqid = api.input['id'] if api.input.has_key('id') else None

    # TODO: check X-Request-User and X-Request-Sign headers and validate the request
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


@api.route('/<cmd>', methods=['GET','POST'])
@auth.login_required
def _default(cmd):
    # TODO: implement the REST API for requests like /api/<model.method>
    return jsonify(dict(command=cmd))
