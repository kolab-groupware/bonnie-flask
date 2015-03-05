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
        print self.env
        ip = self.env['REMOTE_ADDR'] if self.env.has_key('REMOTE_ADDR') else '::1'
        user = str(self.env['REQUEST_USER']) if self.env.has_key('REQUEST_USER') else 'anonymous'
        rand = str(uuid.uuid4())
        dk = hashlib.sha256(ip + rand + user + salt).digest()
        exp = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc) + datetime.timedelta(hours=2)
        return dict(key=binascii.hexlify(dk), expires=exp.isoformat())
