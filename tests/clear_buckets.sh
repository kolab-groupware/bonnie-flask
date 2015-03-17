#!/usr/bin/python
import riak

RIAK_HOST = 'localhost'
RIAK_PORT = 10018

client = riak.RiakClient(http_port=RIAK_PORT, host=RIAK_HOST, protocol='http')

buckets = [
    client.bucket_type("egara-unique").bucket("users-current"),
    client.bucket_type("egara-unique").bucket("imap-folders-current"),
    client.bucket_type("egara-lww").bucket("users"),
    client.bucket_type("egara-lww").bucket("imap-events"),
    client.bucket_type("egara-lww").bucket("imap-folders"),
    client.bucket_type("egara-lww").bucket("imap-message-timeline")
]

for bucket in buckets:
    for keys in bucket.stream_keys():
        for key in keys:
            print('Deleting %s' % key)
            bucket.delete(key)
