import app, flask
from twisted.trial import unittest
from app import storage
from app.model.kolabobject import KolabObject

class FlaskApp(object):
    config = dict()

class TestModel(unittest.TestCase):

    def setUp(self):
        # create stubs for some global objects
        self.patch(storage, 'factory', self._mock_storage)
        self.patch(flask, 'current_app', FlaskApp())

    def _mock_storage(self):
        return storage.AbstractStorage()

    def test_kolabobject_resolve_mailbox_uri(self):
        env = { 'REQUEST_USER': 'john.doe@example.org' }
        ko = KolabObject(env)

        self.assertEqual(ko._resolve_mailbox_uri(None), None)
        self.assertEqual(ko._resolve_mailbox_uri('INBOX'), 'user/john.doe@example.org')
        self.assertEqual(ko._resolve_mailbox_uri('Calendar'), 'user/john.doe/Calendar@example.org')
        self.assertEqual(ko._resolve_mailbox_uri('Other Users/lucy.meyer/Calendar/Personal'), 'user/lucy.meyer/Calendar/Personal@example.org')
        self.assertEqual(ko._resolve_mailbox_uri('Shared Folders/shared/Resource Room 101'), 'shared/Resource Room 101@example.org')

        self.assertEqual(ko._resolve_mailbox_uri('user/john.doe/Calendar@example.org'), 'user/john.doe/Calendar@example.org')
        self.assertEqual(ko._resolve_mailbox_uri('shared/Resource Room 101@example.org'), 'shared/Resource Room 101@example.org')

    def test_kolabobject_convert_mailbox_uri(self):
        env = { 'REQUEST_USER': 'john.doe@example.org' }
        ko = KolabObject(env)

        self.assertEqual(ko._convert_mailbox_uri(None), None)
        self.assertEqual(ko._convert_mailbox_uri('user/john.doe@example.org'), 'INBOX')
        self.assertEqual(ko._convert_mailbox_uri('user/john.doe/Calendar@example.org'), 'Calendar')
        self.assertEqual(ko._convert_mailbox_uri('user/lucy.meyer/Calendar/Personal@example.org'), 'Other Users/lucy.meyer/Calendar/Personal')
        self.assertEqual(ko._convert_mailbox_uri('shared/Resource Room 101@example.org'), 'Shared Folders/shared/Resource Room 101')
