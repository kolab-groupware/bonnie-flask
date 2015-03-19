import httplib, json, base64, hmac, hashlib, email
from twisted.trial import unittest

class TestAPI(unittest.TestCase):
    reqid = 0

    # test config
    config = {
        'api_host': '127.0.0.1',
        'api_port': 8080,
        'api_user': 'webclient',
        'api_pass': 'Welcome2KolabSystems',
        'api_secret': '8431f19170e7f90d4107bf4b169baf'
    }

    @classmethod
    def setUp(self):
        # TODO: reset riak buckets and fill with sample data
        # TODO: fire up the web service
        pass

    def _api_request(self, user, method, sign=True, **kwargs):
        """
            Helper method to send JSON-RPC calls to the API
        """
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(self.config['api_user'] + ':' + self.config['api_pass']),
            'Content-type': "application/json",
            'X-Request-User': user
        }

        self.rpcerror = None
        self.reqid += 1
        body = {
            'jsonrpc': '2.0',
            'id': self.reqid,
            'method': method,
            'params': kwargs
        }
        sbody = json.dumps(body)

        if sign:
            headers['X-Request-Sign'] = hmac.new(
                key=self.config['api_secret'],
                msg=headers.get('X-Request-User') + ':' + sbody,
                digestmod=hashlib.sha256
            ).hexdigest()

        try:
            conn = httplib.HTTPConnection(self.config['api_host'], self.config['api_port'])
            conn.request('POST', '/api/rpc', sbody, headers)

            result = None
            response = conn.getresponse()
            if response.status == 200:
                result = json.loads(response.read())
                if result.has_key('error'):
                    self.rpcerror = result['error']
                if result.has_key('result') and result.has_key('id') and result['id'] == self.reqid:
                    return result['result']

            # print "JSON-RPC response: %d %s; %r" % (response.status, response.reason, result)

        except Exception, e:
            print "JSON-RPC error: %r" % (e)

        return False

    def assertRPCError(self, code=None):
        self.assertIsInstance(self.rpcerror, dict)
        if code is not None:
            self.assertEqual(self.rpcerror['code'], code)

    def test_001_json_rpc(self):
        res = self._api_request('', 'system.keygen', sign=False)
        self.assertFalse(res)
        self.assertRPCError(-32600)

        res = self._api_request('', 'system.keygen', sign=True)
        self.assertIsInstance(res, dict)
        self.assertTrue(res.has_key('key'))
        self.assertTrue(res.has_key('expires'))

    def test_002_invalid_request(self):
        res = self._api_request('john.doe@example.org', 'event.bogus',
            uid='6EE0570E8CA21DDB67FC9ADE5EE38E7F-XXXXXXXXXXXXXXX'
        )
        self.assertFalse(res)
        self.assertRPCError(-32601)  # Method not found

        res = self._api_request('john.doe@example.org', 'event.created',
            uid='6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271'
        )
        self.assertFalse(res)
        self.assertRPCError(-32602)  # Invalid params

        res = self._api_request('john.doe@example.org', 'event.created',
            uid='6EE0570E8CA21DDB67FC9ADE5EE38E7F-INVALID-UID',
            mailbox='Calendar'
        )
        self.assertFalse(res)

    def test_003_created_lastmodified(self):
        created = self._api_request('john.doe@example.org', 'event.created',
            uid='6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271',
            mailbox='Testing',
            msguid=2
        )
        self.assertIsInstance(created, dict)
        self.assertTrue(created.has_key('date'))
        self.assertTrue(created.has_key('user'))
        self.assertTrue(created.has_key('rev'))
        self.assertIn('john.doe@example.org', created['user'])

        changed = self._api_request('john.doe@example.org', 'event.lastmodified',
            uid='6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271',
            mailbox='Testing'
        )
        self.assertIsInstance(changed, dict)
        self.assertTrue(changed.has_key('rev'))

        self.assertTrue(changed['rev'] > created['rev'])
        self.assertTrue(changed['date'] > created['date'])

    def test_004_changelog(self):
        changelog = self._api_request('john.doe@example.org', 'event.changelog',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar',
            msguid=22
        )
        # print json.dumps(changelog, indent=4)
        self.assertIsInstance(changelog, dict)
        self.assertTrue(changelog.has_key('changes'))
        self.assertTrue(changelog.has_key('uid'))
        self.assertEqual(len(changelog['changes']), 2)

        one = changelog['changes'][0]
        two = changelog['changes'][1]
        self.assertTrue(two['rev'] > one['rev'])

    def test_005_get_revision(self):
        changelog = self._api_request('john.doe@example.org', 'event.changelog',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar'
        )
        self.assertIsInstance(changelog, dict)
        self.assertEqual(len(changelog.get('changes', [])), 2)

        rev1 = self._api_request('john.doe@example.org', 'event.get',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar',
            rev=changelog['changes'][0]['rev']
        )
        self.assertIsInstance(rev1, dict)
        self.assertTrue(rev1.has_key('xml'))
        self.assertNotIn('<location>', rev1['xml'])

        rev2 = self._api_request('john.doe@example.org', 'event.get',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar',
            rev=changelog['changes'][1]['rev']
        )
        self.assertIsInstance(rev2, dict)
        self.assertTrue(rev2.has_key('xml'))
        self.assertIn('<text>Somewhere else</text>', rev2['xml'])

        msgdata = self._api_request('john.doe@example.org', 'event.rawdata',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar',
            rev=changelog['changes'][0]['rev']
        )
        self.assertIsInstance(msgdata, unicode)

        message = email.message_from_string(msgdata.encode('utf8','replace'))
        self.assertIsInstance(message, email.message.Message)
        self.assertTrue(message.is_multipart())

    def test_006_diff(self):
        changelog = self._api_request('john.doe@example.org', 'event.changelog',
            uid='5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271',
            mailbox='Calendar'
        )
        self.assertIsInstance(changelog, dict)
        self.assertEqual(len(changelog.get('changes', [])), 2)
        rev1 = changelog['changes'][0]['rev']
        rev2 = changelog['changes'][1]['rev']

        diff = self._api_request('john.doe@example.org', 'event.diff',
            uid=changelog['uid'],
            mailbox='Calendar',
            rev1=rev1,
            rev2=rev2
        )
        # print json.dumps(diff, indent=4)
        self.assertIsInstance(diff, dict)
        self.assertTrue(diff.has_key('changes'))
        self.assertTrue(diff.has_key('uid'))
        self.assertEqual(len(diff['changes']), 6)

    def test_007_diff_instance(self):
        changelog = self._api_request('john.doe@example.org', 'event.changelog',
            uid='8B3B2C54C5218FC09EBC840E6289F5E5-A4BF5BBB9FEAA271',
            mailbox='Calendar'
        )
        self.assertIsInstance(changelog, dict)
        self.assertEqual(len(changelog.get('changes', [])), 2)

        rev1 = changelog['changes'][0]['rev']
        rev2 = changelog['changes'][1]['rev']

        diff = self._api_request('john.doe@example.org', 'event.diff',
            uid=changelog['uid'],
            mailbox='Calendar',
            rev1=rev1,
            rev2=rev2,
            instance='20150324T210000'
        )
        self.assertIsInstance(diff, dict)
        self.assertTrue(diff.has_key('instance'))
        self.assertEqual(len(diff['changes']), 1)  # no change (except lastmodified-date) in this instance

        diff = self._api_request('john.doe@example.org', 'event.diff',
            uid=changelog['uid'],
            mailbox='Calendar',
            rev1=rev1,
            rev2=rev2,
            instance='20150325T210000'
        )
        self.assertIsInstance(diff, dict)
        self.assertEqual(len(diff['changes']), 4) # changes for start,end,sequence,lastmodified-date

        diff = self._api_request('john.doe@example.org', 'event.diff',
            uid=changelog['uid'],
            mailbox='Calendar',
            rev1=rev1,
            rev2=rev2,
            instance='20150330T210000'
        )
        self.assertFalse(diff)
        self.assertRPCError(-32603)  # report error for invalid instance
