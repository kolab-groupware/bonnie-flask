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

import logging, datetime, urllib, urlparse, time

from riak import RiakClient
from riak.mapreduce import RiakKeyFilter, RiakMapReduce
from dateutil.parser import parse as parse_date
from caching import CachedDict
from flask import current_app
from . import AbstractStorage

conf = current_app.config
log = logging.getLogger('storage')

current_time_ms = lambda: int(round(time.time() * 1000))

class RiakStorage(AbstractStorage):

    bucket_types = {
        'users':         'egara-lww',
        'users-current': 'egara-unique',
        'imap-events':   'egara-lww',
        'imap-folders':  'egara-lww',
        'imap-folders-current':  'egara-unique',
        'imap-message-timeline': 'egara-lww'
    }

    def __init__(self, *args, **kw):
        riak_host = 'localhost'
        riak_port = 8098

        self.client = RiakClient(
            protocol='http',
            host=conf['STORAGE'].get('riak_host', riak_host),
            http_port=conf['STORAGE'].get('riak_port', riak_port)
        )
        self.client.set_decoder('application/octet-stream', self._decode_binary)
        self.users_cache = CachedDict(ttl=10)

    def _decode_binary(self, data):
        return str(data).encode("utf-8")

    def _get_bucket(self, bucketname):
        _type = self.bucket_types.get(bucketname, None)
        if _type:
            return self.client.bucket_type(_type).bucket(bucketname)

        return None


    def get(self, key, index, doctype=None, fields=None, **kw):
        """
            Standard API for accessing key/value storage
        """
        result = None
        log.debug("Riak get key %r from %r", key, index)

        try:
            bucket = self._get_bucket(index)
            res = bucket.get(key)
            if res and res.data:
                result = res.data

        except Exception, e:
            log.warning("Riak exception: %s", str(e))
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
            log.warning("Riak exception: %s", str(e))
            result = None

        return result

    def _get_keyfilter(self, index, starts_with=None, ends_with=None, sortby=None, limit=None):
        """
            Helper function to execute a key filter query
        """
        results = None
        fs = None
        fe = None

        if starts_with is not None:
            fs = RiakKeyFilter().starts_with(starts_with)
        if ends_with is not None:
            fe = RiakKeyFilter().ends_with(ends_with)

        if fs and fe:
            keyfilter = fs & fe
        else:
            keyfilter = fs or fe

        return self._mapreduce_keyfilter(index, keyfilter, sortby, limit)

    def _mapreduce_keyfilter(self, index, keyfilter, sortby=None, limit=None):
        """
            Helper function to execute a map-reduce query using the given key filter
        """
        results = None
        log.debug("Riak query %r with key filter %r", index, keyfilter)

        mapred = RiakMapReduce(self.client)
        mapred.add_bucket(self._get_bucket(index))
        mapred.add_key_filters(keyfilter)
        # custom Riak.mapValuesJson() function that also adds the entry key to the data structure
        mapred.map("""
            function(value, keyData, arg) {
                if (value.not_found) {
                    return [value];
                }
                var _data, data = value["values"][0]["data"];
                if (Riak.getClassName(data) !== "Array") {
                    _data = JSON.parse(data);
                    _data["_key"] = value.key;
                    return [_data];
                }
                else {
                    return data
                }
            }
        """)

        if sortby is not None:
            comp = '<' if limit is not None and limit < 0 else '>'
            mapred.reduce_sort('function(a,b){ return (a.%s || 0) %s (b.%s || 0) ? 1 : 0; }' % (sortby, comp, sortby))

        if limit is not None:
            mapred.reduce_limit(abs(limit))

        try:
            results = mapred.run()

        except Exception, e:
            log.warning("Riak MapReduce exception: %s", str(e))
            results = None

        return results

    def get_user(self, id=None, username=None):
        """
            API for resolving usernames and reading user info
        """
        cache_key = id or username

        # check for cached result
        self.users_cache.expunge()
        if cache_key and self.users_cache.has_key(cache_key):
            log.debug("get_user: return cached value for %r", cache_key)
            return self.users_cache[cache_key]

        # search by ID using a key filter
        if id is not None:
            results = self._get_keyfilter('users', starts_with=id + '::', limit=1)
            if results and len(results) > 0:
                self.users_cache[cache_key] = results[0]
                return results[0]

        elif username is not None:
            user = self.get(username, 'users-current')
            if user is not None:
                self.users_cache[cache_key] = user
                return user

            # TODO: query 'users' bucket with an ends_with key filter

        return None

    def get_folder(self, mailbox=None, user=None):
        """
            API for finding IMAP folders and their unique identifiers
        """
        folder_id = self.get(mailbox, 'imap-folders-current')
        if folder_id is not None:
            return dict(uri=mailbox, id=folder_id)

        return None

    def get_events(self, objuid, mailbox, msguid, limit=None):
        """
            API for querying event notifications
        """
        # 1. get timeline entries for current folder
        folder = self.get_folder(mailbox)

        if folder is None:
            log.info("Folder %r not found in storage", mailbox)
            return None;

        object_event_keys = self._get_timeline_keys(objuid, folder['id'], length=3)

        # sanity check with msguid
        if msguid is not None:
            key_prefix = 'message::%s::%s' % (folder['id'], str(msguid))
            if len([k for k in object_event_keys if k.startswith(key_prefix)]) == 0:
                log.warning("Sanity check failed: requested msguid %r not in timeline keys %r", msguid, object_event_keys)
                # TODO: abort?

        # 3. read each corresponding entry from imap-events
        _start = current_time_ms()
        log.debug("Querying imap-events for keys %r", object_event_keys)

        # use keyfilters combined with OR (slower than direct get() calls)
        results = None
        filters = None
        for key in object_event_keys:
            f = RiakKeyFilter().starts_with(key)
            if filters is None:
                filters = f
            else:
                filters |= f

        if filters is not None:
            results = self._mapreduce_keyfilter('imap-events', filters, sortby='timestamp_utc', limit=limit)
            log.debug("Done in %d ms", current_time_ms() - _start)

        return [self._transform_result(x, 'imap-events') for x in results if x.has_key('event') and not x['event'] == 'MessageExpunge'] \
             if results is not None else results

    def _get_timeline_keys(self, objuid, folder_id, length=3):
        """
            Helper method to fetch timeline keys recursively following moves accross folders
        """
        object_event_keys = []

        results = self._get_keyfilter('imap-message-timeline', starts_with='message::' + folder_id + '::', ends_with='::' + objuid)
        if not results or len(results) == 0:
            log.info("No timeline entry found for %r in folder %r", objuid, folder_id)
            return object_event_keys;

        for rec in results:
            key = '::'.join(rec['_key'].split('::', 4)[0:length])
            object_event_keys.append(key)

            # follow moves and add more <folder-id>::<message-id> tuples to our list
            if rec.has_key('history') and isinstance(rec['history'], dict) and rec['history'].has_key('imap'):
                old_folder_id = rec['history']['imap'].get('previous_folder', None)
                if old_folder_id:
                    object_event_keys += self._get_timeline_keys(objuid, old_folder_id, length)

        return object_event_keys

    def get_revision(self, objuid, mailbox, msguid, rev):
        """
            API to get a certain revision of a stored object
        """
        # resolve mailbox first
        folder = self.get_folder(mailbox)
        if folder is None:
            log.info("Folder %r not found in storage", mailbox)
            return None;

        # expand revision into the ISO timestamp format
        try:
            ts = datetime.datetime.strptime(str(rev), "%Y%m%d%H%M%S%f")
            timestamp = ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[0:23]
        except Exception, e:
            log.warning("Invalid revision %r for object %r: %r", rev, objuid, e)
            return None

        # query message-timeline entries starting at peak with current folder (aka mailbox)
        object_event_keys = self._get_timeline_keys(objuid, folder['id'], length=4)

        # get the one key matching the revision timestamp
        keys = [k for k in object_event_keys if '::' + timestamp in k]
        log.debug("Get revision entry %r from candidates %r", timestamp, object_event_keys)

        if len(keys) == 1:
            result = self.get(keys[0], 'imap-events')
            if result is not None:
                return self._transform_result(result, 'imap-events')
        else:
            log.info("Revision timestamp %r doesn't match a single key from: %r", timestamp, object_event_keys)

        return None

    def get_message_data(self, rec):
        """
            Getter for the full IMAP message payload for the given event record
            as previously fetched with get_events() or get_revision()
        """
        return rec.get('message', None)

    def _transform_result(self, result, index):
        """
            Turn an imap-event record into a dict to match the storage API
        """
        result['_index'] = index

        # derrive (numeric) revision from timestamp
        if result.has_key('timestamp_utc') and result.get('event','') in ['MessageAppend','MessageMove']:
            try:
                ts = parse_date(result['timestamp_utc'])
                result['revision'] = ts.strftime("%Y%m%d%H%M%S%f")[0:17]
            except:
                pass

        # extract folder name from uri
        if result.has_key('uri') and not result.has_key('mailbox'):
            uri = self._parse_imap_uri(result['uri'])

            username = uri['user']
            domain = uri['domain']
            folder_name = uri['path']
            folder_path = uri['path']
            imap_delimiter = '/'

            if not username == None:
                if folder_name == "INBOX":
                    folder_path = imap_delimiter.join(['user', '%s@%s' % (username, domain)])
                else:
                    folder_path = imap_delimiter.join(['user', username, '%s@%s' % (folder_name, domain)])

            result['mailbox'] = folder_path

            if not result.has_key('uidset') and uri.has_key('UID'):
                result['uidset'] = uri['UID']

        return result

    def _parse_imap_uri(self, uri):
        """
            Split the given URI string into its components
        """
        split_uri = urlparse.urlsplit(uri)

        if len(split_uri.netloc.split('@')) == 3:
            (username, domain, server) = split_uri.netloc.split('@')
        elif len(split_uri.netloc.split('@')) == 2:
            (username, server) = split_uri.netloc.split('@')
            domain = None
        elif len(split_uri.netloc.split('@')) == 1:
            username = None
            domain = None
            server = split_uri.netloc

        result = dict(user=username, domain=domain, host=server)

        # First, .path == '/Calendar/Personal%20Calendar;UIDVALIDITY=$x[/;UID=$y]
        # Take everything after the first slash, and omit any INBOX/ stuff.
        path_str = '/'.join([x for x in split_uri.path.split('/') if not x == 'INBOX'][1:])
        path_arr = path_str.split(';')
        result['path'] = urllib.unquote(path_arr[0])

        # parse the path/query parameters into a dict
        param = dict()
        for p in path_arr[1:]:
            if '=' in p:
                (key,val) = p.split('=', 2)
                result[key] = urllib.unquote(val)

        return result
