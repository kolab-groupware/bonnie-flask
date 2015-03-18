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
from dateutil.parser import parse as parse_date
from pykolab.xml.utils import compute_diff
from collections import OrderedDict
from email import message_from_string
from app import storage

log = logging.getLogger('model.kolabobject')

class KolabObject(object):
    """
        Base Model class for accessing Kolab Groupware Object data
    """
    folder_type = 'unknown'
    x_kolab_type = 'application/x-vnd.kolab.*'

    def __init__(self, env={}):
        from flask import current_app

        self.env = env
        self.config = current_app.config
        self.storage = storage.factory()

    def created(self, uid, mailbox, msguid=None):
        """
            Provide created date and user
        """
        changelog = self._object_changelog(uid, mailbox, msguid, 1)
        if changelog and len(changelog) > 0:
            for change in changelog:
                if change['op'] == 'APPEND':
                    change['uid'] = uid
                    change.pop('op', None)
                    return change

        return False

    def lastmodified(self, uid, mailbox, msguid=None):
        """
            Provide last change information
        """
        changelog = self._object_changelog(uid, mailbox, msguid, -3)
        if changelog and len(changelog) > 0:
            for change in changelog:
                if change['op'] == 'APPEND':
                    change['uid'] = uid
                    change.pop('op', None)
                    return change

        return False

    def changelog(self, uid, mailbox, msguid=None):
        """
            Full changelog
        """
        changelog = self._object_changelog(uid, mailbox, msguid)
        if changelog:
            return dict(uid=uid, changes=changelog)

        return False

    def get(self, uid, rev, mailbox, msguid=None):
        """
            Retrieve an old revision
        """
        obj = self._get(uid, mailbox, msguid, rev)

        if obj is not None:
            return dict(uid=uid, rev=rev, xml=str(obj), mailbox=mailbox)

        return False

    def _get(self, uid, mailbox, msguid, rev):
        """
            Get an old revision and return the pykolab.xml object
        """
        obj = False

        rec = self.storage.get_revision(uid, self._resolve_mailbox_uri(mailbox), msguid, rev)

        if rec is not None:
            raw = self.storage.get_message_data(rec)
            try:
                message = message_from_string(raw.encode('utf8','replace'))
                obj = self._object_from_message(message) or False
            except Exception, e:
                log.warning("Failed to parse mime message for UID %s @%s: %r", uid, rev, e)

            if obj is False:
                log.warning("Failed to parse mime message for UID %s @%s", uid, rev)

        return obj

    def diff(self, uid, rev, mailbox, msguid=None):
        """
            Compare two revisions of an object and return a list of property changes
        """
        r = str(rev).split(':')
        rev_old = int(r[0])
        rev_new = int(r[-1])

        if rev_old >= rev_new:
            raise ValueError("Invalid argument 'rev'")

        old = self._get(uid, mailbox, msguid, rev_old)
        if old == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_old))

        new = self._get(uid, mailbox, msguid, rev_new)
        if new == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_new))

        return dict(uid=uid, rev=rev_new, changes=convert2primitives(compute_diff(old.to_dict(), new.to_dict(), True)))

    def rawdata(self, uid, mailbox, rev, msguid=None):
        """
            Get the full message payload of an old revision
        """
        rec = self.storage.get_revision(uid, self._resolve_mailbox_uri(mailbox), msguid, rev)
        if rec is not None:
            return self.storage.get_message_data(rec)

        return False

    def _object_from_message(self, message):
        """
             To be implemented in derived classes
        """
        return None

    def _object_changelog(self, uid, mailbox, msguid, limit=None):
        """
            Query storage for changelog events related to the given UID
        """
        # this requires a user context
        if not self.env.has_key('REQUEST_USER') or not self.env['REQUEST_USER']:
            return None

        # fetch event log from storage
        eventlog = self.storage.get_events(uid, self._resolve_mailbox_uri(mailbox), msguid, limit)

        # convert logstash entries into a sane changelog
        event_op_map = {
            'MessageNew': 'APPEND',
            'MessageAppend': 'APPEND',
            'MessageTrash': 'DELETE',
            'MessageMove': 'MOVE',
        }
        last_append_uid = 0
        result = []

        if eventlog is not None:
            for log in eventlog:
                # filter MessageTrash following a MessageAppend event (which is an update operation)
                if log['event'] == 'MessageTrash' and last_append_uid > int(log['uidset']):
                    continue

                # remember last appended message uid
                if log['event'] == 'MessageAppend' and log.has_key('uidset'):
                    last_append_uid = int(log['uidset'])

                # compose log entry to return
                logentry = {
                    'rev': log.get('revision', None),
                    'op': event_op_map.get(log['event'], 'UNKNOWN'),
                    'mailbox': self._convert_mailbox_uri(log.get('mailbox', None))
                }
                try:
                    timestamp = parse_date(log['timestamp'])
                    logentry['date'] = datetime.datetime.strftime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                except:
                    logentry['date'] = log['timestamp']

                # TODO: translate mailbox identifier back to a relative folder path?

                logentry['user'] = self._get_user_info(log)

                result.append(logentry)

        return result

    def _resolve_username(self, user):
        """
            Resovle the given username to the corresponding nsuniqueid from LDAP
        """
        # find existing entry in our storage backend
        result = self.storage.get_user(username=user)

        if result and result.has_key('id'):
            # TODO: cache this lookup in memory?
            return result['id']

        # fall-back: return md5 sum of the username to make usernames work as fields/keys in elasticsearch
        return hashlib.md5(user).hexdigest()

    def _get_user_info(self, rec):
        """
            Return user information (name, email) related to the given log entry
        """
        if rec.has_key('user_id'):
            # get real user name from rec['user_id']
            user = self.storage.get_user(id=rec['user_id'])
            if user is not None:
                return "%(cn)s <%(user)s>" % user

        if rec.has_key('user'):
            return rec['user']

        elif rec['event'] == 'MessageAppend' and rec['headers'].has_key('From'):
            # fallback to message headers
            return rec['headers']['From'][0]

        return 'unknown'

    def _resolve_mailbox_uri(self, mailbox):
        """
            Convert the given mailbox string into an absolute URI
            regarding the context of the requesting user.
        """
        # this requires a user context
        if not self.env.has_key('REQUEST_USER') or not self.env['REQUEST_USER']:
            return mailbox

        if mailbox is None:
            return None

        # mailbox already is an absolute path
        if mailbox.startswith('user/') or mailbox.startswith('shared/'):
            return mailbox

        domain = ''
        user = self.env['REQUEST_USER']
        if '@' in user:
            (user,_domain) = user.split('@', 1)
            domain = '@' + _domain

        owner = user
        path = '/' + mailbox

        # TODO: make this configurable or read from IMAP
        shared_prefix = 'Shared Folders/'
        others_prefix = 'Other Users/'
        imap_delimiter = '/'

        # case: shared folder
        if mailbox.startswith(shared_prefix):
            return mailbox[len(shared_prefix):] + domain

        # case: other users folder
        if mailbox.startswith(others_prefix):
            (owner, subpath) = mailbox[len(others_prefix):].split(imap_delimiter, 1)
            path = imap_delimiter + subpath

        if mailbox.upper() == 'INBOX':
            path = ''

        # default: personal namespace folder
        return 'user/' + owner + path + domain

    def _convert_mailbox_uri(self, mailbox):
        """
            Convert the given absolute mailbox URI into a relative folder
            name regarding the context of the requesting user.
        """
        if mailbox is None:
            return None

        # this requires a user context
        request_user = str(self.env.get('REQUEST_USER', '')).lower()

        # TODO: make this configurable or read from IMAP
        shared_prefix = 'Shared Folders'
        others_prefix = 'Other Users'
        imap_delimiter = '/'
        domain = ''

        if '@' in mailbox:
            (folder,domain) = mailbox.split('@', 1)
        else:
            folder = mailbox

        if folder.startswith('user/'):
            parts = folder.split(imap_delimiter, 2)
            if len(parts) > 2:
                (prefix,user,path) = parts
            else:
                (prefix,user) = parts
                path = ''

            if len(path) == 0:
                path = 'INBOX'

            if not (user + '@' + domain).lower() == request_user:
                folder = imap_delimiter.join([others_prefix, user, path])
            else:
                folder = path

        elif folder.startswith('shared/'):
            folder = imap_delimiter.join([shared_prefix, folder])

        return folder


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
