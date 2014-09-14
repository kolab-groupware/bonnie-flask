import os
import json
import pytz
import datetime
from collections import OrderedDict
from flask import current_app


class KolabObject(object):
    """
        Base Model class for accessing Kolab Groupware Object data
    """
    def __init__(self, env={}):
        self.env = env
        self.config = current_app.config

    def created(self, uid, mailbox=None):
        """
            Provide created date and user
        """
        data = self._object_data(uid)
        if data and data.has_key('changes'):
            for change in data['changes']:
                if change['rev'] == 1:
                    return dict(uid=uid, date=change['date'], user=change['user'], mailbox=change['mailbox'])

        return False

    def lastmodified(self, uid, mailbox=None):
        """
            Provide last change information
        """
        data = self._object_data(uid)
        if data and data.has_key('changes'):
            data['changes'].reverse()
            for change in data['changes']:
                if change.has_key('date'):
                    change['uid'] = uid
                    change.pop('op', None)
                    return change

        return False

    def changelog(self, uid, mailbox=None):
        """
            Full changelog
        """
        data = self._object_data(uid)
        if data:
            return data

        return False

    def get(self, uid, rev, mailbox=None):
        """
            Retrieve an old revision
        """
        if not mailbox:
            mailbox = 'Calendar'
        filepath = os.path.join(self.config['DATA_DIR'], '%s-%d.xml' % (uid, rev))
        if os.path.isfile(filepath):
            fp = open(filepath,'r')
            xml = fp.read()
            fp.close()
            return dict(uid=uid, rev=rev, xml=xml, mailbox=mailbox)

        return False

    def diff(self, uid, rev, mailbox=None):
        """
            Compare two revisions of an object and return a list of property changes
        """
        r = str(rev).split(':')
        rev_old = int(r[0])
        rev_new = int(r[-1])

        if rev_old >= rev_new:
            raise ValueError("Invalid argument 'rev'")

        a = self.get(uid, rev_old)
        if a == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_old))

        b = self.get(uid, rev_new)
        if b == False:
            raise ValueError("Object %s @rev:%d not found" % (uid, rev_new))

        # get dict representations from the raw XML payload
        old = self._object_dict(a['xml'])
        new = self._object_dict(b['xml'])

        return dict(uid=uid, rev=rev_new, changes=convert2primitives(get_diff(old, new)))

    def _object_dict(self, raw):
        """
             To be implemented in derived classes
        """
        return None

    def _object_data(self, uid):
        data = None
        filepath = os.path.join(self.config['DATA_DIR'], '%s.json' % (uid))
        if os.path.isfile(filepath):
            fp = open(filepath,'r')
            try:
                data = json.loads(fp.read())
            except:
                data = None
            fp.close()

        return data



#####  Utility functions for comparing object revisions


def get_diff(a, b):
    """
        List the differences between two given dicts
    """
    diff = []

    properties = a.keys()
    properties.extend([x for x in b.keys() if x not in properties])

    for prop in properties:
        aa = a[prop] if a.has_key(prop) else None
        bb = b[prop] if b.has_key(prop) else None

        # compare two lists
        if isinstance(aa, list) or isinstance(bb, list):
            if not isinstance(aa, list):
                aa = [aa]
            if not isinstance(bb, list):
                bb = [bb]
            index = 0
            length = max(len(aa), len(bb))
            while index < length:
                aai = aa[index] if index < len(aa) else None
                bbi = bb[index] if index < len(bb) else None
                if not compare_values(aai, bbi):
                    (old, new) = reduce_properties(aai, bbi)
                    diff.append(OrderedDict([('property', prop), ('index', index), ('old', old), ('new', new)]))
                index += 1

        # the two properties differ
        elif not compare_values(aa, bb):
            (old, new) = reduce_properties(aa, bb)
            diff.append(OrderedDict([('property', prop), ('old', old), ('new', new)]))

    return diff


def compare_values(aa, bb):
    ignore_keys = ['rsvp']
    if not aa.__class__ == bb.__class__:
        return False

    if isinstance(aa, dict) and isinstance(bb, dict):
        aa = dict(aa)
        bb = dict(bb)
        # ignore some properties for comparison
        for k in ignore_keys:
            aa.pop(k, None)
            bb.pop(k, None)

    return aa == bb


def reduce_properties(aa, bb):
    """
        Compares two given structs and removes equal values in bb
    """
    if not isinstance(aa, dict) or not isinstance(bb, dict):
        return (aa, bb)

    properties = aa.keys()
    properties.extend([x for x in bb.keys() if x not in properties])

    for prop in properties:
        if not aa.has_key(prop) or not bb.has_key(prop):
            continue
        if isinstance(aa[prop], dict) and isinstance(bb[prop], dict):
            (aa[prop], bb[prop]) = reduce_properties(aa[prop], bb[prop])
        if aa[prop] == bb[prop]:
            # del aa[prop]
            del bb[prop]

    return (aa, bb)


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
