#!/bin/sh

RIAK_HOST='localhost'
RIAK_PORT='10018'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-unique/buckets/users-current/keys/john.doe@example.org" \
 -H 'Content-Type: application/json' \
 -d '{
    "dn": "uid=doe,ou=People,dc=example,dc=org",
    "cn": "Doe, John",
    "user": "john.doe@example.org",
    "id": "55475201-bdc211e4-881c96ef-f248ab46"
 }'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/users/keys/55475201-bdc211e4-881c96ef-f248ab46::2015-03-07T14:10:16.941541::john.doe@example.org" \
 -H 'Content-Type: application/json' \
 -d '{
    "dn": "uid=doe,ou=People,dc=example,dc=org",
    "cn": "Doe, John",
    "user": "john.doe@example.org",
    "id": "55475201-bdc211e4-881c96ef-f248ab46"
 }'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-unique/buckets/imap-folders-current/keys/user%2Fjohn.doe%2FCalendar%40example.org" \
 -H 'Content-Type: application/octet-stream' \
 -d 'a5660caa-3165-4a84-bacd-ef4b58ef3663'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::3::2015-03-04T09:11:39.711Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageAppend",
    "vnd.cmu.envelope": "(...)",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "body": "--=_2bf2e936dd4806dab1e774f4bf4cb5b5\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_2bf2e936dd4806dab1e774f4bf4cb5b5\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1950\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-02T23:13:57Z</date-time></created><dtstamp><date-time>2015-03-02T23:52:22Z</date-time></dtstamp><sequence><integer>2</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-03T12:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-03T14:00:00</date-time></dtend><summary><text>Todays Egara Testing</text></summary><location><text>kolab34.example.org</text></location><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_2bf2e936dd4806dab1e774f4bf4cb5b5--",
    "bodyStructure": "(...)",
    "service": "imap",
    "modseq": 2,
    "timestamp": "2015-03-04T09:11:39.711Z",
    "pid": 28071,
    "vnd.cmu.sessionId": "kolab34.example.org-28071-1425478299-1-14630748386624877725",
    "messages": 1,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960274/;UID=3",
    "uidset": "3",
    "messageSize": 2843,
    "uidnext": 4,
    "user": "john.doe@example.org",
    "vnd.cmu.unseenMessages": 1,
    "vnd.cmu.midset": [ "NIL" ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_2bf2e936dd4806dab1e774f4bf4cb5b5\"",
        "Subject": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271",
        "From": "john.doe@example.org",
        "To": "john.doe@example.org",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::3::2015-03-04T09:11:39.711Z::6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::4::2015-03-04T21:56:46.465Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageAppend",
    "vnd.cmu.envelope": "(...)", 
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46", 
    "body": "--=_fc7d881734b2f8b6cf99458899d79664\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_fc7d881734b2f8b6cf99458899d79664\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1950\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-02T23:13:57Z</date-time></created><dtstamp><date-time>2015-03-05T02:56:46Z</date-time></dtstamp><sequence><integer>3</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-05T13:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-05T15:00:00</date-time></dtend><summary><text>Todays Egara Testing</text></summary><location><text>kolab34.example.org</text></location><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_fc7d881734b2f8b6cf99458899d79664--",
    "bodyStructure": "(...)", 
    "service": "imap", 
    "modseq": 9, 
    "timestamp": "2015-03-04T21:56:46.465Z", 
    "pid": 981, 
    "vnd.cmu.sessionId": "kolab34.example.org-981-1425524206-1-5416454962879660084", 
    "messages": 2, 
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330/;UID=4", 
    "uidset": "4", 
    "messageSize": 2910, 
    "uidnext": 5, 
    "user": "john.doe@example.org", 
    "vnd.cmu.unseenMessages": 2, 
    "vnd.cmu.midset": [ "NIL" ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_fc7d881734b2f8b6cf99458899d79664\"",
        "Subject": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271",
        "From": "john.doe@example.org",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::4::2015-03-04T21:56:46.465Z::6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::3::2015-03-04T21:56:46.500Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageTrash",
    "uidset": "3", 
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "service": "imap",
    "modseq": 10,
    "timestamp": "2015-03-04T21:56:46.500Z",
    "pid": 981,
    "vnd.cmu.sessionId": "kolab34.example.org-981-1425524206-1-5416454962879660084",
    "messages": 2,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330",
    "uidnext": 5,
    "user": "john.doe@example.org",
    "vnd.cmu.unseenMessages": 2,
    "vnd.cmu.midset": [ "NIL" ],
    "headers": {
        "Subject": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271",
        "From": "john.doe@example.org",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T15:58:43.016000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "body": "--=_c54c7baa744029b81ae04981de13c8b5\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_c54c7baa744029b81ae04981de13c8b5\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1960\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-17T15:58:42Z</date-time></created><dtstamp><date-time>2015-03-17T15:58:42Z</date-time></dtstamp><sequence><integer>0</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T11:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T13:00:00</date-time></dtend><summary><text>Thursday Test</text></summary><description><text>This is a test event for Egara</text></description><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_c54c7baa744029b81ae04981de13c8b5--\r\n", 
    "bodyStructure": "((\"TEXT\" \"PLAIN\" (\"CHARSET\" \"ISO-8859-1\") NIL NIL \"QUOTED-PRINTABLE\" 206 4 NIL NIL NIL NIL)(\"APPLICATION\" \"CALENDAR+XML\" (\"CHARSET\" \"UTF-8\" \"NAME\" \"kolab.xml\") NIL NIL \"8BIT\" 1960 NIL (\"ATTACHMENT\" (\"FILENAME\" \"kolab.xml\" \"SIZE\" \"1960\")) NIL NIL) \"MIXED\" (\"BOUNDARY\" \"=_c54c7baa744029b81ae04981de13c8b5\") NIL NIL NIL)", 
    "event": "MessageAppend",
    "flags": [
        "\\Recent"
    ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_c54c7baa744029b81ae04981de13c8b5\"",
        "Date": "Tue, 17 Mar 2015 15:58:42 +0000",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }, 
    "messageSize": 2920,
    "messages": 4,
    "modseq": 57,
    "pid": 1579,
    "service": "imap",
    "timestamp": "2015-03-17T15:58:43.016000Z",
    "uidnext": 22,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330/;UID=21",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Tue, 17 Mar 2015 15:58:42 +0000\" \"5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-1579-1426607922-1-10050682032034970758",
    "vnd.cmu.unseenMessages": 4
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T15:58:43.016000Z::5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::22::2015-03-17T17:17:37.514000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "body": "--=_e8dedd96d48a3bdb20e76ee77e234363\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_e8dedd96d48a3bdb20e76ee77e234363\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=2123\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n\r\n  <vcalendar>\r\n    <properties>\r\n      <prodid>\r\n        <text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text>\r\n      </prodid>\r\n      <version>\r\n        <text>2.0</text>\r\n      </version>\r\n      <x-kolab-version>\r\n        <text>3.1.0</text>\r\n      </x-kolab-version>\r\n    </properties>\r\n    <components>\r\n      <vevent>\r\n        <properties>\r\n          <uid>\r\n            <text>5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271</text>\r\n          </uid>\r\n          <created>\r\n            <date-time>2015-03-17T15:58:42Z</date-time>\r\n          </created>\r\n          <dtstamp>\r\n            <date-time>2015-03-17T17:17:37Z</date-time>\r\n          </dtstamp>\r\n          <sequence>\r\n            <integer>1</integer>\r\n          </sequence>\r\n          <class>\r\n            <text>PUBLIC</text>\r\n          </class>\r\n          <dtstart>\r\n            <parameters>\r\n              <tzid>\r\n                <text>/kolab.org/Europe/Berlin</text>\r\n              </tzid>\r\n            </parameters>\r\n            <date-time>2015-03-19T10:00:00</date-time>\r\n          </dtstart>\r\n          <dtend>\r\n            <parameters>\r\n              <tzid>\r\n                <text>/kolab.org/Europe/Berlin</text>\r\n              </tzid>\r\n            </parameters>\r\n            <date-time>2015-03-19T11:00:00</date-time>\r\n          </dtend>\r\n          <summary>\r\n            <text>Thursday Test</text>\r\n          </summary>\r\n          <description>\r\n            <text>This is a test event for Egara</text>\r\n          </description>\r\n          <status>\r\n            <text>CONFIRMED</text>\r\n          </status>\r\n          <location>\r\n            <text>Somewhere else</text>\r\n          </location>\r\n          <organizer>\r\n            <parameters>\r\n              <cn>\r\n                <text>Doe, John</text>\r\n              </cn>\r\n            </parameters>\r\n            <cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address>\r\n          </organizer>\r\n        </properties>\r\n      </vevent>\r\n    </components>\r\n  </vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_e8dedd96d48a3bdb20e76ee77e234363--\r\n", 
    "bodyStructure": "((\"TEXT\" \"PLAIN\" (\"CHARSET\" \"ISO-8859-1\") NIL NIL \"QUOTED-PRINTABLE\" 206 4 NIL NIL NIL NIL)(\"APPLICATION\" \"CALENDAR+XML\" (\"CHARSET\" \"UTF-8\" \"NAME\" \"kolab.xml\") NIL NIL \"8BIT\" 2123 NIL (\"ATTACHMENT\" (\"FILENAME\" \"kolab.xml\" \"SIZE\" \"2123\")) NIL NIL) \"MIXED\" (\"BOUNDARY\" \"=_e8dedd96d48a3bdb20e76ee77e234363\") NIL NIL NIL)", 
    "event": "MessageAppend",
    "flags": [
        "\\Recent"
    ], 
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_e8dedd96d48a3bdb20e76ee77e234363\"",
        "Date": "Tue, 17 Mar 2015 17:17:37 +0000",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }, 
    "messageSize": 3083,
    "messages": 5,
    "modseq": 58,
    "pid": 7493,
    "service": "imap",
    "timestamp": "2015-03-17T17:17:37.514000Z",
    "uidnext": 23,
    "uidset": "22",
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330/;UID=22",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Tue, 17 Mar 2015 17:17:37 +0000\" \"5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)", 
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-7493-1426612657-1-6878020795100368520",
    "vnd.cmu.unseenMessages": 5
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::22::2015-03-17T17:17:37.514000Z::5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT 'http://localhost:10018/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T17:17:37.562000Z' \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageExpunge",
    "messages": 4,
    "modseq": 60,
    "pid": 7493,
    "service": "imap",
    "timestamp": "2015-03-17T17:17:37.562000Z",
    "uidnext": 23,
    "uidset": "21",
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-7493-1426612657-1-6878020795100368520",
    "vnd.cmu.unseenMessages": 4
}'

curl -XPUT 'http://localhost:10018/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T17:17:37.554000Z' \
    -H 'Content-Type: application/json' \
    -d '{
    "event": "MessageTrash",
    "messages": 5,
    "modseq": 59,
    "pid": 7493,
    "service": "imap",
    "timestamp": "2015-03-17T17:17:37.554000Z",
    "uidnext": 23,
    "uidset": "21",
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-7493-1426612657-1-6878020795100368520",
    "vnd.cmu.unseenMessages": 5
}'
