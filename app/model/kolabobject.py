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
import pytz
import hashlib
import datetime
import logging
from dateutil.parser import parse
from pykolab.xml.utils import compute_diff
from collections import OrderedDict
from email import message_from_string
from flask import current_app
from app import storage

log = logging.getLogger('model.kolabobject')

class KolabObject(object):
    """
        Base Model class for accessing Kolab Groupware Object data
    """
    folder_type = 'unknown'
    x_kolab_type = 'application/x-vnd.kolab.*'

    def __init__(self, env={}):
        self.env = env
        self.config = current_app.config
        self.storage = storage.factory()

    def created(self, uid, mailbox=None):
        """
            Provide created date and user
        """
        changelog = self._object_changelog(uid, 1)
        if changelog and len(changelog) > 0:
            for change in changelog:
                if change['op'] == 'APPEND':
                    change['uid'] = uid
                    change.pop('op', None)
                    return change

        return False

    def lastmodified(self, uid, mailbox=None):
        """
            Provide last change information
        """
        changelog = self._object_changelog(uid, -3)
        if changelog and len(changelog) > 0:
            for change in changelog:
                if change['op'] == 'APPEND':
                    change['uid'] = uid
                    change.pop('op', None)
                    return change

        return False

    def changelog(self, uid, mailbox=None):
        """
            Full changelog
        """
        changelog = self._object_changelog(uid)
        if changelog:
            return dict(uid=uid, changes=changelog)

        return False

    def get(self, uid, rev, mailbox=None):
        """
            Retrieve an old revision
        """
        obj = self._get(uid, rev)

        if obj is not None:
            return dict(uid=uid, rev=rev, xml=str(obj), mailbox=mailbox)

        return False

    def _get(self, uid, rev):
        """
            Get an old revision and return the pykolab.xml object
        """
        obj = False

        # get a list of folders the request user has access
        folders = self._user_permitted_folders('name')

        if len(folders) > 0:
            folder_ids = [x['_id'] for x in folders]

            # retrieve the log entry matching the given uid and revision
            results = self.storage.select(
                query=[
                    ('headers.Subject', '=', uid),
                    ('headers.X-Kolab-Type', '=', self.x_kolab_type),
                    ('folder_id', '=', folder_ids),
                    ('revision', '=', rev)
                ],
                index='logstash-*',
                doctype='logs',
                fields='event,revision,uidset,folder_id,message',
                limit=1
            )

            if results and results['total'] > 0:
                for rec in results['hits']:
                    if rec.has_key('message'):
                        try:
                            message = message_from_string(rec['message'].encode('utf8','replace'))
                            obj = self._object_from_message(message) or False
                        except Exception, e:
                            log.warning("Failed to parse mime message for UID %s @%s: %r", uid, rev, e)
                            continue

                        if obj is False:
                            break
                        else:
                            log.warning("Failed to parse mime message for UID %s @%s", uid, rev)

        return obj

    def diff(self, uid, rev, mailbox=None):
        """
            Compare two revisions of an object and return a list of property changes
        """
        r = str(rev).split(':')
        rev_old = int(r[0])
        rev_new = int(r[-1])

        if rev_old >= rev_new:
            raise ValueError("Invalid argument 'rev'")

        old = self._get(uid, rev_old)
        if old == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_old))

        new = self._get(uid, rev_new)
        if new == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_new))

        return dict(uid=uid, rev=rev_new, changes=convert2primitives(compute_diff(old.to_dict(), new.to_dict(), True)))

    def _object_from_message(self, message):
        """
             To be implemented in derived classes
        """
        return None

    def _user_permitted_folders(self, fields='uniqueid,name'):
        """
            Get a list of folders the request user has access
        """
        # this requires a user context
        if not self.env.has_key('REQUEST_USER') or not self.env['REQUEST_USER']:
            return []

        # translate the given username into its nsuiniqueid
        userid = self._resolve_username(self.env['REQUEST_USER'])

        # get a list of folders the request user has access
        folders = self.storage.select(
            query=[
                ('type', '=', self.folder_type),
                ('OR', [
                    ('acl.anyone',  '~', 'lr*'),
                    ('acl.'+userid, '~', 'lr*')
                ])
            ],
            index='objects',
            doctype='folder',
            fields=fields
        )

        return folders['hits'] if folders and folders['total'] > 0 else []

    def _object_changelog(self, uid, limit=None):
        """
            Query storage for changelog events related to the given UID
        """
        # this requires a user context
        if not self.env.has_key('REQUEST_USER') or not self.env['REQUEST_USER']:
            return None

        result = None

        # get a list of folders the request user has access
        folders = self._user_permitted_folders('name')

        if len(folders) > 0:
            folder_ids = [x['_id'] for x in folders]
            folder_names = dict((x['_id'],x['name']) for x in folders)

            # set sorting and resultset size
            sortcol = '@timestamp'
            if limit is not None and limit < 0:
                sortcol = sortcol + ':desc'
                limit = abs(limit)

            # search for events related to the given uid and the permitted folders
            eventlog = self.storage.select(
                query=[
                    ('headers.Subject', '=', uid),
                    ('headers.X-Kolab-Type', '=', self.x_kolab_type),
                    ('folder_id', '=', folder_ids)
                ],
                index='logstash-*',
                doctype='logs',
                sortby=sortcol,
                fields='event,revision,headers,uidset,folder_id,user,user_id,@timestamp',
                limit=limit
            )

            # convert logstash entries into a sane changelog
            event_op_map = {
                'MessageNew': 'APPEND',
                'MessageAppend': 'APPEND',
                'MessageTrash': 'DELETE',
                'MessageMove': 'MOVE',
            }
            last_append_uid = 0
            result = []
            if eventlog and eventlog['total'] > 0:
                for log in eventlog['hits']:
                    # filter MessageTrash following a MessageAppend event (which is an update operation)
                    if log['event'] == 'MessageTrash' and last_append_uid > int(log['uidset']):
                        continue

                    # remember last appended message uid
                    if log['event'] == 'MessageAppend' and log.has_key('uidset'):
                        last_append_uid = int(log['uidset'])

                    # compose log entry to return
                    logentry = {
                        'rev': int(log['revision']) if log.has_key('revision') else None,
                        'op': event_op_map.get(log['event'], 'UNKNOWN'),
                        'mailbox': folder_names.get(log['folder_id'], None)
                    }
                    try:
                        timestamp = parse(log['@timestamp'])
                        logentry['date'] = datetime.datetime.strftime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        logentry['date'] = log['@timestamp']

                    logentry['user'] = self._get_user_info(log)

                    result.append(logentry)

        return result

    def _resolve_username(self, user):
        """
            Resovle the given username to the corresponding nsuniqueid from LDAP
        """
        # find existing entry in our storage backend
        result = self.storage.select(
            [ ('user', '=', user) ],
            index='objects',
            doctype='user',
            sortby='@timestamp:desc',
            limit=1
        )

        if result and result['total'] > 0:
            # TODO: cache this lookup in memory?
            return result['hits'][0]['_id']

        # fall-back: return md5 sum of the username to make usernames work as fields/keys in elasticsearch
        return hashlib.md5(user).hexdigest()

    def _get_user_info(self, log):
        """
            Return user information (name, email) related to the given log entry
        """
        if log.has_key('user_id'):
            # get real user name from log['user_id']
            user = self.storage.get(log['user_id'], index='objects', doctype='user')
            if user is not None:
                return "%(cn)s <%(user)s>" % user

        if log.has_key('user'):
            return log['user']

        elif log['event'] == 'MessageAppend' and log['headers'].has_key('From'):
            # fallback to message headers
            return log['headers']['From'][0]

        return 'unknown'


#####  Utility functions


def convert2primitives(struct):
    """
        Convert complex types like datetime into primitives which can be serialized into JSON
    """
    out = None
    if isinstance(struct, datetime.datetime):
        tz = 'Z' if struct.tzinfo == pytz.utc else '%z'
        out = struct.strftime('%Y-%m-%dT%H:%M:%S' + tz)
    elif isinstance(struct, datetime.date):
        out = struct.strftime('%Y-%m-%d')
    elif isinstance(struct, list):
        out = [convert2primitives(x) for x in struct]
    elif isinstance(struct, OrderedDict):
        out = OrderedDict([(key,convert2primitives(struct[key])) for key in struct.keys()])
    elif isinstance(struct, dict):
        out = dict(zip(struct.keys(), map(convert2primitives, struct.values())))
    else:
        out = struct

    return out
