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


def factory():
    """
        Factory function to return the right storage backend instance
    """
    # TODO: make storage backend configurable
    # currently Elasticsearch is the only backend available
    from elasticsearch_storage import ElasticseachStorage
    return ElasticseachStorage()
