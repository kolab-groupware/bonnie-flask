import logging
from flask import jsonify, request
from . import api
from .. import model
from authentication import auth, permission_required
from ..model import Permission

reqid = None
log = logging.getLogger('api')

@api.route('/rpc', methods=['GET','POST'])
@auth.login_required
@permission_required(Permission.API_ACCESS)
def rpc():
    """
        Endpoint for JSON-RPC calls

        Example POST /api/rpc
        { "jsonrpc": "2.0", "method": "object.diff", "params": { "uid":"0015c5fe-9baf-0561-ffff", "rev": "1:2" }, "id": 1 }

    """
    global reqid

    if api.input.has_key('jsonrpc') and api.input['jsonrpc'] == '2.0':
        reqid = api.input['id'] if api.input.has_key('id') else None
        method = api.input['method'] if api.input.has_key('method') else ''
        params = api.input['params'] if api.input.has_key('params') else dict()

        log.debug("JSON-RPC call (%s) from %s: %s(%r)" % (reqid, request.remote_addr, method, params))
        res = _exec_api_call(method, params)
        log.debug("JSON-RPC result (%s) for %s: %r" % (reqid, request.remote_addr, res))
        return jsonify(dict(jsonrpc="2.0", result=res, id=reqid))

    else:
        raise JsonRPCException(-32600, "Invalid Request")


def _exec_api_call(method, params):
    """
        Dispatches API calls to the according model object
    """
    m = method.split('.')

    if not isinstance(params, dict):
        raise JsonRPCException(-32600, "Invalid params: only named parameters are allowed")

    elif len(m) == 2:
        (classname, func) = m

        # don't exec private methods (starting with _)
        if func[0] == '_':
            raise JsonRPCException(-32601, "Method not found")

        obj = model.get_instance(classname, env=request.env)
        if obj and hasattr(obj, func):
            try:
                return getattr(obj, func)(**params)

            except Exception, e:
                log.debug(traceback.format_exc())
                raise JsonRPCException(-32603, str(e))

    # fall through the above checks
    raise JsonRPCException(-32601, "Method not found")



class JsonRPCException(Exception):
    """
        JSON-RPC error class
    """
    def __init__(self, code, msg, data=None):
        self.code = code
        self.message = msg
        self.data = data
        super(JsonRPCException, self).__init__(msg)


@api.errorhandler(JsonRPCException)
def json_rpc_error(e):
    """
        Compose a valid JSON-RPC error struct
    """
    # log error
    log.error("JSON-RPC exception (%s) from %s: (%d) %s; %r" % (
        reqid, request.remote_addr, e.code, e, request.body
    ))

    err = dict(code=e.code, message=str(e))
    response = jsonify(dict(jsonrpc="2.0", error=err, id=reqid))
    # response.status_code = 500
    return response
