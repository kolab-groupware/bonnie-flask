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
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_2bf2e936dd4806dab1e774f4bf4cb5b5\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271\r\n\r\n--=_2bf2e936dd4806dab1e774f4bf4cb5b5\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_2bf2e936dd4806dab1e774f4bf4cb5b5\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1950\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-02T23:13:57Z</date-time></created><dtstamp><date-time>2015-03-02T23:52:22Z</date-time></dtstamp><sequence><integer>2</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-03T12:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-03T14:00:00</date-time></dtend><summary><text>Todays Egara Testing</text></summary><location><text>kolab34.example.org</text></location><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_2bf2e936dd4806dab1e774f4bf4cb5b5--",
    "bodyStructure": "(...)",
    "service": "imap",
    "modseq": 2,
    "timestamp": "2015-03-04T09:11:39.711+00:00",
    "timestamp_utc": "2015-03-04T09:11:39.711Z",
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
    },
    "groupware_uid": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271"
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
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_fc7d881734b2f8b6cf99458899d79664\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271\r\n\r\n--=_fc7d881734b2f8b6cf99458899d79664\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_fc7d881734b2f8b6cf99458899d79664\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1950\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-02T23:13:57Z</date-time></created><dtstamp><date-time>2015-03-05T02:56:46Z</date-time></dtstamp><sequence><integer>3</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-05T13:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-05T15:00:00</date-time></dtend><summary><text>Todays Egara Testing</text></summary><location><text>kolab34.example.org</text></location><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_fc7d881734b2f8b6cf99458899d79664--",
    "bodyStructure": "(...)", 
    "service": "imap", 
    "modseq": 9, 
    "timestamp": "2015-03-04T21:56:46.465+00:00", 
    "timestamp_utc": "2015-03-04T21:56:46.465Z", 
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
    },
    "groupware_uid": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271"
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
    "timestamp": "2015-03-04T21:56:46.500+00:00",
    "timestamp_utc": "2015-03-04T21:56:46.500Z",
    "pid": 981,
    "vnd.cmu.sessionId": "kolab34.example.org-981-1425524206-1-5416454962879660084",
    "messages": 2,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330",
    "uidnext": 5,
    "user": "john.doe@example.org",
    "vnd.cmu.unseenMessages": 2,
    "vnd.cmu.midset": [ "NIL" ]
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T15:58:43.016000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_c54c7baa744029b81ae04981de13c8b5\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271\r\n\r\n--=_c54c7baa744029b81ae04981de13c8b5\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_c54c7baa744029b81ae04981de13c8b5\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1960\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-17T15:58:42Z</date-time></created><dtstamp><date-time>2015-03-17T15:58:42Z</date-time></dtstamp><sequence><integer>0</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T11:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T13:00:00</date-time></dtend><summary><text>Thursday Test</text></summary><description><text>This is a test event for Egara</text></description><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_c54c7baa744029b81ae04981de13c8b5--\r\n", 
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
    "timestamp": "2015-03-17T15:58:43.016+00:00",
    "timestamp_utc": "2015-03-17T15:58:43.016000Z",
    "uidnext": 22,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330/;UID=21",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Tue, 17 Mar 2015 15:58:42 +0000\" \"5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-1579-1426607922-1-10050682032034970758",
    "vnd.cmu.unseenMessages": 4,
    "groupware_uid": "5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T15:58:43.016000Z::5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::22::2015-03-17T17:17:37.514000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_e8dedd96d48a3bdb20e76ee77e234363\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271\r\n\r\n--=_e8dedd96d48a3bdb20e76ee77e234363\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_e8dedd96d48a3bdb20e76ee77e234363\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=2123\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.2</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-17T15:58:42Z</date-time></created><dtstamp><date-time>2015-03-17T17:17:37Z</date-time></dtstamp><sequence><integer>1</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T10:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-19T11:00:00</date-time></dtend><summary><text>Thursday Test</text></summary><description><text>This is a test event for Egara</text></description><status><text>CONFIRMED</text></status><location><text>Somewhere else</text></location><organizer><parameters><cn><text>Doe, John</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_e8dedd96d48a3bdb20e76ee77e234363--\r\n",
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
    "timestamp": "2015-03-17T17:17:37.514+00:00",
    "timestamp_utc": "2015-03-17T17:17:37.514000Z",
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
    "vnd.cmu.unseenMessages": 5,
    "groupware_uid": "5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::22::2015-03-17T17:17:37.514000Z::5A637BE7895D785671E1732356E65CC8-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T17:17:37.562000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageExpunge",
    "messages": 4,
    "modseq": 60,
    "pid": 7493,
    "service": "imap",
    "timestamp": "2015-03-17T17:17:37.562+00:00",
    "timestamp_utc": "2015-03-17T17:17:37.562000Z",
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

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::a5660caa-3165-4a84-bacd-ef4b58ef3663::21::2015-03-17T17:17:37.554000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageTrash",
    "messages": 5,
    "modseq": 59,
    "pid": 7493,
    "service": "imap",
    "timestamp": "2015-03-17T17:17:37.554+00:00",
    "timestamp_utc": "2015-03-17T17:17:37.554000Z",
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

# move event to folder Testing

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-unique/buckets/imap-folders-current/keys/user%2Fjohn.doe%2FTesting%40example.org" \
 -H 'Content-Type: application/octet-stream' \
 -d 'fe0137f5-6828-474f-9cf6-fdf135123679'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::1::2015-03-18T04:13:31.158000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageMove",
    "messages": 1,
    "modseq": 3,
    "oldMailboxID": "imap://john.doe@example.org@kolab34.example.org/Calendar;UIDVALIDITY=1424960330",
    "pid": 12489,
    "service": "imap",
    "timestamp": "2015-03-18T04:13:31.158+00:00",
    "timestamp_utc": "2015-03-18T04:13:31.158000Z",
    "uidnext": 2,
    "uidset": "1",
    "uri": "imap://john.doe@example.org@kolab34.example.org/Testing;UIDVALIDITY=1426651436",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_8e9630d5eb4cee74209f3d6f1736c0b5\"",
        "Date": "Wed, 18 Mar 2015 14:13:07 +0100",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    },
    "vnd.cmu.oldUidset": "4",
    "vnd.cmu.sessionId": "kolab34.example.org-12489-1426652010-1-1342732898036616806",
    "vnd.cmu.unseenMessages": 1,
    "groupware_uid": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::1::2015-03-18T04:13:31.158000Z::6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{
    "history": {
        "imap": {
            "previous_folder": "a5660caa-3165-4a84-bacd-ef4b58ef3663", 
            "previous_id": "4"
        }
    }
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::2::2015-03-18T04:13:31.454000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_8e9630d5eb4cee74209f3d6f1736c0b5\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271\r\n\r\n--=_8e9630d5eb4cee74209f3d6f1736c0b5\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_8e9630d5eb4cee74209f3d6f1736c0b5\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=1950\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.1</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-02T23:13:57Z</date-time></created><dtstamp><date-time>2015-03-18T13:35:07Z</date-time></dtstamp><sequence><integer>13</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-17T13:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-17T15:00:00</date-time></dtend><summary><text>Todays Egara Testing</text></summary><location><text>kolab34.example.org</text></location><organizer><parameters><cn><text>John Doe</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_8e9630d5eb4cee74209f3d6f1736c0b5--\r\n",
    "bodyStructure": "(...)",
    "event": "MessageAppend",
    "flags": [
        "\\Recent"
    ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_8e9630d5eb4cee74209f3d6f1736c0b5\"",
        "Date": "Wed, 18 Mar 2015 14:35:07 +0100",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }, 
    "messageSize": 2910,
    "messages": 2,
    "modseq": 4,
    "pid": 12489,
    "service": "imap",
    "timestamp": "2015-03-18T04:13:31.454+00:00",
    "timestamp_utc": "2015-03-18T04:13:31.454000Z",
    "uidnext": 3,
    "uidset": "2",
    "uri": "imap://john.doe@example.org@kolab34.example.org/Testing;UIDVALIDITY=1426651436/;UID=2",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Wed, 18 Mar 2015 14:35:07 +0100\" \"6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-12489-1426652010-1-1342732898036616806",
    "vnd.cmu.unseenMessages": 2,
    "groupware_uid": "6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::2::2015-03-18T04:13:31.454000Z::6EE0570E8CA21DDB67FC9ADE5EE38E7F-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::1::2015-03-18T04:13:31.467000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "event": "MessageTrash", 
    "messages": 2, 
    "modseq": 5, 
    "pid": 12489, 
    "service": "imap", 
    "timestamp": "2015-03-18T04:13:31.467+00:00", 
    "timestamp_utc": "2015-03-18T04:13:31.467000Z", 
    "uidnext": 3, 
    "uidset": "1", 
    "uri": "imap://john.doe@example.org@kolab34.example.org/Testing;UIDVALIDITY=1426651436", 
    "user": "john.doe@example.org", 
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46", 
    "vnd.cmu.midset": [
        "NIL"
    ], 
    "vnd.cmu.sessionId": "kolab34.example.org-12489-1426652010-1-1342732898036616806", 
    "vnd.cmu.unseenMessages": 2
}'

# new event with attachment
curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::3::2015-03-18T04:32:29.376000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_03f3c3e51790c8ff68ca5414a293ae51\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271\r\n\r\n--=_03f3c3e51790c8ff68ca5414a293ae51\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_03f3c3e51790c8ff68ca5414a293ae51\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=2195\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.1</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-18T13:54:05Z</date-time></created><dtstamp><date-time>2015-03-18T13:54:05Z</date-time></dtstamp><sequence><integer>0</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-20T16:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-20T17:00:00</date-time></dtend><summary><text>Attachments Test</text></summary><organizer><parameters><cn><text>John Doe</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer><attach><parameters><fmttype><text>text/plain</text></fmttype><x-label><text>attachment.txt</text></x-label></parameters><uri>cid:attachment.1426686845.2073.txt</uri></attach></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_03f3c3e51790c8ff68ca5414a293ae51\r\nContent-ID: <attachment.1426686845.2073.txt>\r\nContent-Transfer-Encoding: base64\r\nContent-Type: text/plain;\r\n name=attachment.txt\r\nContent-Disposition: attachment;\r\n filename=attachment.txt;\r\n size=37\r\n\r\nVGhpcyBpcyBhIHRleHQgYXR0YWNobWVudCAodmVyc2lvbiAxKQ==\r\n--=_03f3c3e51790c8ff68ca5414a293ae51--\r\n",
    "bodyStructure": "(...)",
    "event": "MessageAppend",
    "flags": [
        "\\Recent"
    ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_03f3c3e51790c8ff68ca5414a293ae51\"",
        "Date": "Wed, 18 Mar 2015 14:54:05 +0100",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    }, 
    "messageSize": 3450,
    "messages": 2,
    "modseq": 7,
    "pid": 12618,
    "service": "imap",
    "timestamp": "2015-03-18T04:32:29.376+00:00",
    "timestamp_utc": "2015-03-18T04:32:29.376000Z",
    "uidset": 3,
    "uidnext": 4,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Testing;UIDVALIDITY=1426651436/;UID=3",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Wed, 18 Mar 2015 14:54:05 +0100\" \"390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-12618-1426653149-1-11265804361548763525",
    "vnd.cmu.unseenMessages": 2,
    "groupware_uid": "390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::3::2015-03-18T04:32:29.376000Z::390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-events/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::4::2015-03-18T04:36:34.162000Z" \
 -H 'Content-Type: application/json' \
 -d '{
    "message": "MIME-Version: 1.0\r\nContent-Type: multipart/mixed;\r\n boundary=\"=_531f398ebbeecbf523661f67827bea1e\"\r\nFrom: john.doe@example.org\r\nTo: john.doe@example.org\r\nX-Kolab-Type: application/x-vnd.kolab.event\r\nX-Kolab-Mime-Version: 3.0\r\nSubject: 390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271\r\n\r\n--=_531f398ebbeecbf523661f67827bea1e\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=ISO-8859-1\r\n\r\nThis is a Kolab Groupware object. To view this object you will need an emai=\r\nl client that understands the Kolab Groupware format. For a list of such em=\r\nail clients please visit http://www.kolab.org/\r\n\r\n\r\n--=_531f398ebbeecbf523661f67827bea1e\r\nContent-Transfer-Encoding: 8bit\r\nContent-Type: application/calendar+xml; charset=UTF-8;\r\n name=kolab.xml\r\nContent-Disposition: attachment;\r\n filename=kolab.xml;\r\n size=2195\r\n\r\n<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\r\n<icalendar xmlns=\"urn:ietf:params:xml:ns:icalendar-2.0\">\r\n<vcalendar><properties><prodid><text>Roundcube-libkolab-1.1 Libkolabxml-1.1</text></prodid><version><text>2.0</text></version><x-kolab-version><text>3.1.0</text></x-kolab-version></properties><components><vevent><properties><uid><text>390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271</text></uid><created><date-time>2015-03-18T13:54:05Z</date-time></created><dtstamp><date-time>2015-03-18T13:58:09Z</date-time></dtstamp><sequence><integer>0</integer></sequence><class><text>PUBLIC</text></class><dtstart><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-20T16:00:00</date-time></dtstart><dtend><parameters><tzid><text>/kolab.org/Europe/Berlin</text></tzid></parameters><date-time>2015-03-20T17:00:00</date-time></dtend><summary><text>Attachments Test</text></summary><organizer><parameters><cn><text>John Doe</text></cn></parameters><cal-address>mailto:%3Cjohn.doe%40example.org%3E</cal-address></organizer><attach><parameters><fmttype><text>text/plain</text></fmttype><x-label><text>attachment.txt</text></x-label></parameters><uri>cid:attachment.1426687089.9628.txt</uri></attach></properties></vevent></components></vcalendar>\r\n\r\n</icalendar>\r\n\r\n--=_531f398ebbeecbf523661f67827bea1e\r\nContent-ID: <attachment.1426687089.9628.txt>\r\nContent-Transfer-Encoding: base64\r\nContent-Type: text/plain;\r\n name=attachment.txt\r\nContent-Disposition: attachment;\r\n filename=attachment.txt;\r\n size=56\r\n\r\nVGhpcyBpcyBhIHRleHQgYXR0YWNobWVudCAodmVyc2lvbiAyKQp3aXRoIGEgc2Vjb25kIGxpbmU=\r\n--=_531f398ebbeecbf523661f67827bea1e--\r\n",
    "bodyStructure": "(...)",
    "event": "MessageAppend",
    "flags": [
        "\\Recent"
    ],
    "headers": {
        "Content-Type": "multipart/mixed; boundary=\"=_531f398ebbeecbf523661f67827bea1e\"",
        "Date": "Wed, 18 Mar 2015 14:58:10 +0100",
        "From": "john.doe@example.org",
        "MIME-Version": "1.0",
        "Subject": "390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271",
        "To": "john.doe@example.org",
        "X-Kolab-Mime-Version": "3.0",
        "X-Kolab-Type": "application/x-vnd.kolab.event"
    },
    "messageSize": 3474,
    "messages": 3,
    "modseq": 8,
    "pid": 12671,
    "service": "imap",
    "timestamp": "2015-03-18T04:36:34.162+00:00",
    "timestamp_utc": "2015-03-18T04:36:34.162000Z",
    "uidset": 4,
    "uidnext": 5,
    "uri": "imap://john.doe@example.org@kolab34.example.org/Testing;UIDVALIDITY=1426651436/;UID=4",
    "user": "john.doe@example.org",
    "user_id": "55475201-bdc211e4-881c96ef-f248ab46",
    "vnd.cmu.envelope": "(\"Wed, 18 Mar 2015 14:58:10 +0100\" \"390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271\" ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) ((NIL NIL \"john.doe\" \"example.org\")) NIL NIL NIL NIL)",
    "vnd.cmu.midset": [
        "NIL"
    ],
    "vnd.cmu.sessionId": "kolab34.example.org-12671-1426653393-1-5448614388380127124",
    "vnd.cmu.unseenMessages": 3,
    "groupware_uid": "390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271"
}'

curl -XPUT "http://$RIAK_HOST:$RIAK_PORT/types/egara-lww/buckets/imap-message-timeline/keys/message::fe0137f5-6828-474f-9cf6-fdf135123679::4::2015-03-18T04:36:34.162000Z::390582E807A257686D51A6BF87F342E9-A4BF5BBB9FEAA271" \
 -H 'Content-Type: application/json' \
 -d '{}'


