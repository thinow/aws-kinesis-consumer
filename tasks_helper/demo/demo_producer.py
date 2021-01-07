import json
import random
import time

import boto3
import invoke
from botocore.config import Config


class DemoProducer:

    @classmethod
    def run(cls, runner: invoke.Runner, endpoint: str, stream_name: str):
        runner.run('docker-compose up -d')

        kinesis = cls.connect(endpoint)

        cls.create_stream(kinesis, stream_name)

        while True:
            cls.produce_value(kinesis, stream_name)
            time.sleep(0.2)

    @classmethod
    def produce_value(cls, kinesis, stream_name):
        value = random.randint(1_000, 10_000)
        kinesis.put_record(
            StreamName=stream_name,
            PartitionKey=str(value),
            Data=json.dumps({
                'status': 'OK',
                'value': value,
            })
        )
        print(f'record produced with value={value}')

    @classmethod
    def connect(cls, endpoint):
        kinesis = boto3.client(
            'kinesis',
            endpoint_url=endpoint,
            config=Config(region_name='eu-central-1'),
            aws_access_key_id='any',
            aws_secret_access_key='any',
            aws_session_token='any'
        )
        return kinesis

    @classmethod
    def create_stream(cls, kinesis, stream_name):
        try:
            kinesis.create_stream(StreamName=stream_name, ShardCount=2)
        except:
            # ignore error when the stream already exists, or any other error
            pass
