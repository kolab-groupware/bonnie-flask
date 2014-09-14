import uuid, hashlib, binascii, datetime, pytz
from flask import current_app

class System(object):
    """
        Model class handling system.* API calls
    """
    def __init__(self, env={}):
        self.env = env
        self.config = current_app.config

    def keygen(self, salt='salt'):
        ip = self.env['REMOTE_ADDR'] if self.env.has_key('REMOTE_ADDR') else '::1'
        user = self.env['REQUEST_USER'] if self.env.has_key('REQUEST_USER') else 'anonymous'
        rand = str(uuid.uuid4())
        dk = hashlib.sha256(ip + rand + user + salt).digest()
        exp = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc) + datetime.timedelta(hours=2)
        return dict(key=binascii.hexlify(dk), expires=exp.isoformat())

    def _authenticate_user(self, identity):
        """
            Authenticate the given user identification aginst the user database
        """
        username = identity['login']
        return False
