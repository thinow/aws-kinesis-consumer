import random
import time

import boto3
from botocore.config import Config

STREAM = 'foo'

kinesis = boto3.client(
    'kinesis',
    endpoint_url='http://localhost:4567/',
    config=Config(region_name='eu-central-1'),
    aws_access_key_id='any',
    aws_secret_access_key='any',
    aws_session_token='any'
)

try:
    kinesis.create_stream(StreamName=STREAM, ShardCount=2)
except:
    # ignore error when the stream already exists
    pass

for index in range(10_000):
    value = random.randint(1000, 9999)
    kinesis.put_record(
        StreamName=STREAM,
        PartitionKey=str(value),
        Data=str({
            'status': 'OK',
            'value': value,
        }).encode('UTF-8')
    )
    print(f'record produced with value={value}')
    time.sleep(0.2)
