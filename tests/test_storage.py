import os, flask, json, email
from app import storage
from twisted.trial import unittest

class FlaskCurrentApp(object):
    config = dict(
        STORAGE=dict(
            backend='riak',
            riak_host='127.0.0.1',
            riak_port='10018'
        ),
        CONFIG_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config')
    )

    def __init__(self):
        import logging.config
        logging.config.fileConfig(self.config['CONFIG_DIR'] + '/bonnie-flask.conf')


class TestStorage(unittest.TestCase):

    def setUp(self):
        # patch current_app to return static config
        self.patch(flask, 'current_app', FlaskCurrentApp())

    def test_000_instance(self):
        strg = storage.factory()
        self.assertIsInstance(strg, storage.AbstractStorage)
        self.assertIsInstance(strg, storage.riak_storage.RiakStorage)

    def test_001_get_user_by_name(self):
        strg = storage.factory()
        user = strg.get_user(username='john.doe@example.org')
        self.assertIsInstance(user, dict)
        self.assertEqual(user['id'], '55475201-bdc211e4-881c96ef-f248ab46')
        self.assertEqual(user['user'], 'john.doe@example.org')

    def test_002_get_user_by_id(self):
        strg = storage.factory()
        user = strg.get_user(id='55475201-bdc211e4-881c96ef-f248ab46')
        self.assertIsInstance(user, dict)
        self.assertEqual(user['user'], 'john.doe@example.org')
        self.assertEqual(user['id'], '55475201-bdc211e4-881c96ef-f248ab46')

    def test_010_get_folder_id(self):
        strg = storage.factory()
        folder = strg.get_folder('user/john.doe/Calendar@example.org')
        self.assertIsInstance(folder, dict)
        self.assertEqual(folder['id'], 'a5660caa-3165-4a84-bacd-ef4b58ef3663')

    def test_020_get_events(self):
        strg = storage.factory()
        oldmailbox = 'user/john.doe/Calendar@example.org'
        mailbox = 'user/john.doe/Testing@example.org'
        events = strg.get_events('6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271', mailbox, 2)
        self.assertEqual(len(events), 6)
        self.assertEqual(events[0]['event'], 'MessageAppend')
        self.assertEqual(events[0]['uidset'], '3')
        self.assertEqual(events[0]['mailbox'], oldmailbox)
        self.assertEqual(events[1]['event'], 'MessageAppend')
        self.assertEqual(events[1]['uidset'], '4')
        self.assertEqual(events[1]['mailbox'], oldmailbox)
        self.assertEqual(events[2]['event'], 'MessageTrash')
        self.assertEqual(events[2]['uidset'], '3')
        self.assertEqual(events[3]['event'], 'MessageMove')
        self.assertEqual(events[3]['uidset'], '1')
        self.assertEqual(events[4]['event'], 'MessageAppend')
        self.assertEqual(events[4]['uidset'], '2')
        self.assertEqual(events[4]['mailbox'], mailbox)
        self.assertEqual(events[5]['event'], 'MessageTrash')
        self.assertEqual(events[5]['uidset'], '1')
        self.assertEqual(events[5]['mailbox'], mailbox)

    def test_025_get_revision(self):
        strg = storage.factory()
        uid = '5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271'
        mailbox = 'user/john.doe/Calendar@example.org'
        events = strg.get_events(uid, mailbox, None, limit=1)
        self.assertEqual(len(events), 1)

        rec = strg.get_revision(uid, mailbox, None, events[0]['revision'])
        self.assertIsInstance(rec, dict)
        self.assertEqual(rec['event'], 'MessageAppend')

        msgsource = strg.get_message_data(rec)
        self.assertIsInstance(msgsource, unicode)

        message = email.message_from_string(msgsource.encode('utf8','replace'))
        self.assertIsInstance(message, email.message.Message)
        self.assertTrue(message.is_multipart())

