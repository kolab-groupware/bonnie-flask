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

import logging
import elasticsearch

from flask import current_app
from . import AbstractStorage

conf = current_app.config
log = logging.getLogger('storage.elasticsearch')

class ElasticseachStorage(AbstractStorage):

    def __init__(self, *args, **kw):
        elasticsearch_address = 'localhost:9200'

        if conf['STORAGE'].has_key('elasticsearch_address'):
            elasticsearch_address = conf['STORAGE']['elasticsearch_address']

        self.es = elasticsearch.Elasticsearch(elasticsearch_address)


    def get_user(self, id=None, username=None):
        """
            API for resolving usernames and reading user info
        """
        # get user by ID
        if id is not None:
            log.debug("ES get user by ID: %s" % (id), level=8)
            return self.get(id, index='objects', doctype='user')

        # find existing entry in our storage backend
        result = self.select(
            [ ('user', '=', user) ],
            index='objects',
            doctype='user',
            sortby='@timestamp:desc',
            limit=1
        )

        log.debug("ES get user by name: %s; %r" % (username, result), level=8)

        if result and result['total'] > 0:
            return self._transform_result(result['hits'][0])

        return None

    def get_folder(self, mailbox=None, user=None):
        """
            API for finding an IMAP folder record
        """
        # FIXME: revisit this implementation for new storage layout
        # FIXME: check ACL of this folder in regards of the given user

        result = self.select(
            [ ('uri', '=', mailbox) ],
            index='objects',
            doctype='folder',
            sortby='@timestamp:desc',
            limit=1
        )

        if result and result['total'] > 0:
            return self._transform_result(result['hits'][0])

        return None

    def get_events(self, msguid, objuid, mailbox, limit=None):
        """
            API for querying event notifications
        """
        # FIXME: this only fetches events from the given mailbox!
        # TODO: resolve this object trail through all folders, starting with the current one
        folders = []
        folder = mailbox if isinstance(mailbox, dict) else self.get_folder(mailbox)

        if folder is not None:
            folders.append(folder)

        if len(folders) > 0:
            result = []
            folder_ids = [x['id'] for x in folders]
            folder_names = dict((x['id'],x['name']) for x in folders)

            # set sorting and resultset size
            sortcol = '@timestamp'
            if limit is not None and limit < 0:
                sortcol = sortcol + ':desc'
                limit = abs(limit)

            # search for events related to the given uid and the permitted folders
            eventlog = self.storage.select(
                query=[
                    ('headers.Subject', '=', objuid),
                    ('folder_id', '=', folder_ids)
                ],
                index='logstash-*',
                doctype='logs',
                sortby=sortcol,
                fields='event,revision,headers,uidset,folder_id,user,user_id,@timestamp',
                limit=limit
            )

            if eventlog and eventlog['total'] > 0:
                result = eventlog['hits']

            return result

        return None

    def get_revision(self, objuid, mailbox, msguid, rev):
        """
            API to get a certain revision of a stored object
        """
        folder = mailbox if isinstance(mailbox, dict) else self.get_folder(mailbox)

        # retrieve the log entry matching the given uid and revision
        if folder is not None:
            results = self.storage.select(
                query=[
                    ('headers.Subject', '=', uid),
                    ('folder_id', '=', folder['id']),
                    ('revision', '=', rev)
                ],
                index='logstash-*',
                doctype='logs',
                fields='event,revision,uidset,folder_id,message',
                limit=1
            )

            if results and results['total'] > 0:
                return results['hits'][0]:

        return None

    def get(self, key, index, doctype=None, fields=None, **kw):
        """
            Standard API for accessing key/value storage
        """
        try:
            res = self.es.get(
                index=index,
                doc_type=doctype,
                id=key,
                _source_include=fields or '*'
            )
            log.debug("ES get result for %s/%s/%s: %r" % (index, doctype, key, res), level=8)

            if res['found']:
                result = res['_source']
                result['_id'] = res['_id']
                result['_index'] = res['_index']
                result['_doctype'] = res['_type']
            else:
                result = None

        except elasticsearch.exceptions.NotFoundError, e:
            log.debug("ES entry not found for %s/%s/%s: %r" % (index, doctype, key, e))
            result = None

        except Exception, e:
            log.warning("ES get exception: %r", e)
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
        args = dict(index=index, doc_type=doctype, _source_include=fields or '*')

        if isinstance(query, dict):
            args['body'] = query
        elif isinstance(query, list):
            args['q'] = self._build_query(query)
        else:
            args['q'] = query

        if sortby is not None:
            args['sort'] = sortby
        if limit is not None:
            args['size'] = int(limit)

        try:
            res = self.es.search(**args)
            log.debug("ES select result for %r: %r" % (args['q'] or args['body'], res), level=8)

        except elasticsearch.exceptions.NotFoundError, e:
            log.debug("ES entry not found for key %s: %r", key, e)
            res = None

        except Exception, e:
            log.warning("ES get exception: %r", e)
            res = None

        if res is not None and res.has_key('hits'):
            result = dict(total=res['hits']['total'])
            result['hits'] = [self._transform_result(x) for x in res['hits']['hits']]
        else:
            result = None

        return result

    def _build_query(self, params, boolean='AND'):
        """
            Convert the given list of query parameters into a Lucene query string
        """
        query = []
        for p in params:
            if isinstance(p, str):
                # direct query string
                query.append(p)

            elif isinstance(p, tuple) and len(p) == 3:
                # <field> <op> <value> triplet
                (field, op, value) = p
                op_ = '-' if op == '!=' else ''

                if isinstance(value, list):
                    value_ = '("' + '","'.join(value) + '")'
                elif isinstance(value, tuple):
                    value_ = '[%s TO %s]' % value
                else:
                    quote = '"' if not '*' in str(value) else ''
                    value_ = quote + str(value) + quote

                query.append('%s%s:%s' % (op_, field, value_))

            elif isinstance(p, tuple) and len(p) == 2:
                # group/subquery with boolean operator
                (op, subquery) = p
                query.append('(' + self._build_query(subquery, op) + ')')

        return (' '+boolean+' ').join(query)

    def _transform_result(self, res):
        """
            Turn an elasticsearch result item into a simple dict
        """
        result = res['_source'] if res.has_key('_source') else dict()
        result['id'] = res['_id']
        result['_index'] = res['_index']
        result['_doctype'] = res['_type']
        result['_score'] = res['_score']

        if result.has_key('@timestamp'):
            result['timestamp'] = result['@timestamp']
            result.pop('@timestamp', None)

        return result