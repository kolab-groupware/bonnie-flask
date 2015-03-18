# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Kolab Systems AG (http://www.kolabsys.com)
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


class AbstractStorage(object):
    """
        Interface class for abstracted access to storage
    """

    def get(self, key, index, doctype=None, fields=None, **kw):
        """
            Standard API for accessing key/value storage

            @param key:     Primary key of the record to retrieve
            @param index:   Index name (i.e. database name)
            @param doctype: Document type (i.e. table name)
            @param fields:  List of fields to retrieve (string, comma-separated)
        """
        return None

    def set(self, key, value, index, doctype=None, **kw):
        """
            Standard API for writing to key/value storage

            @param key:     Primary key of the record to create/update
            @param value:   The record data as dict with field => value pairs
            @param index:   Index name (i.e. database name)
            @param doctype: Document type (i.e. table name)
        """
        return None

    def select(self, query, index, doctype=None, fields=None, sortby=None, limit=None, **kw):
        """
            Standard API for querying storage

            @param query:   List of query parameters, each represented as a triplet of (<field> <op> <value>).
                            combined to an AND list of search criterias. <value> can either be
                             - a string for direct comparison
                             - a list for "in" comparisons
                             - a tuple with two values for range queries
            @param index:   Index name (i.e. database name)
            @param doctype: Document type (i.e. table name)
            @param fields:  List of fields to retrieve (string, comma-separated)
            @param sortby:  Fields to be used fort sorting the results (string, comma-separated)
            @param limit:   Number of records to return
        """
        return None

    def get_user(self, id=None, username=None):
        """
            API for resolving usernames and reading user info:

            @param id:       Unique identifier for a user record
            @param username: Non-unique username to resolve
        """
        return None

    def get_folder(self, mailbox=None, user=None):
        """
            API for finding an IMAP folder record

            @param mailbox:  Mailbox name
            @param user:     User context
        """
        return None

    def get_events(self, objuid, mailbox, msguid, limit=None):
        """
            API for querying event notifications

            @param objuid:   Groupware object UID
            @param mailbox:  IMAP folder that message/object currently resides in
            @param msguid:   IMAP message UID (the last known)
            @param limit:    Number of records to return (negative number for most recent first)
        """
        return None

    def get_revision(self, objuid, mailbox, msguid, rev):
        """
            API to get a certain revision of a stored object

            @param objuid:   Groupware object UID
            @param mailbox:  IMAP folder that message/object currently resides in
            @param msguid:   IMAP message UID (the last known)
            @param rev:      Revision identifier
        """
        return None

    def get_message_data(self, rec):
        """
            Getter for the full IMAP message payload for the given event record
            as previously fetched with get_events() or get_revision()
        """
        return rec.get('message', None)


def StorageException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def factory():
    """
        Factory function to return the right storage backend instance
    """
    from flask import current_app
    conf = current_app.config

    if conf['STORAGE'].has_key('backend'):
        backend = conf['STORAGE']['backend']
    else:
        backend = 'riak'

    if backend == 'elasticsearch':
        from elasticsearch_storage import ElasticseachStorage
        return ElasticseachStorage()

    elif backend == 'riak':
        from riak_storage import RiakStorage
        return RiakStorage()

    raise StorageException("Invalid backend %r specified" % (backend))
