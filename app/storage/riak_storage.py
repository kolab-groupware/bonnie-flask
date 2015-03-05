# -*- coding: utf-8 -*-
#
# Copyright 2015 Kolab Systems AG (http://www.kolabsys.com)
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

import logging

from riak import RiakClient
from riak.mapreduce import RiakKeyFilter, RiakMapReduce
from flask import current_app
from . import AbstractStorage

conf = current_app.config
log = logging.getLogger('storage.riak')

class RiakStorage(AbstractStorage):

    bucket_types = {
        'users':         'egara-lww',
        'current-users': 'egara-unique',
        'imap-events':   'egara-lww',
        'imap-folders':  'egara-lww'
    }

    def __init__(self, *args, **kw):
        riak_host = 'localhost'
        riak_port = 8098

        if conf['STORAGE'].has_key('riak_host'):
            riak_host = conf['STORAGE']['riak_host']
        if conf['STORAGE'].has_key('riak_port'):
            riak_port = int(conf['STORAGE']['riak_port'])

        self.client = RiakClient(protocol='http', host=riak_host, http_port=riak_port)

    def _get_bucket(self, bucketname):
        _type = self.bucket_types.get(bucketname, None)
        if _type:
            return self.client.bucket_type("egara-lww").bucket(bucketname)

        return None


    def get(self, key, index, doctype=None, fields=None, **kw):
        """
            Standard API for accessing key/value storage
        """
        try:
            result = None

        except Exception, e:
            log.warning("Riak exception: %r", e)
            result = None

        return result

    def set(self, key, value, index, doctype=None, **kw):
        """
            Standard API for writing to key/value storage
        """
        return False

    def select(self, query, index, doctype=None, fields=None, sortby=None, limit=None, **kw):
        """
            Standard API for querying storage
        """
        result = None

        try:
            pass

        except Exception, e:
            log.warning("Riak exception: %r", e)
            res = None

        return result


    def get_user(self, id=None, username=None):
        """
            API for resolving usernames and reading user info
        """
        return None

    def get_folders(self):
        """
            API for finding IMAP folders and their unique identifiers
        """
        return None

    def get_events(self, objuid, mailbox, msguid, limit=None):
        """
            API for querying event notifications
        """
        return None

    def get_revision(self, objuid, mailbox, msguid, rev):
        """
            API to get a certain revision of a stored object
        """
        return None
