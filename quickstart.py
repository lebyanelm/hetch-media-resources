ACCESS_KEY = "EQ0VUP6EPG502OZ60GDW"
SECRET_KEY = "ZHHHhSD787Vc1rkiFyveH41qzpDTeaTq1nhp8Cu3"

import boto
import boto.s3.connection
access_key = 'put your access key here!'
secret_key = 'put your secret key here!'

conn = boto.connect_s3(
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_KEY,
        host = 'eu-central-1.linodeobjects.com',
        #is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

for bucket in conn.get_all_buckets():
    print("{name}\t{created}".format(
        name = bucket.name,
        created = bucket.creation_date,
    ))