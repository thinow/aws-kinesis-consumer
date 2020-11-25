import os
import uuid
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

import boto3
from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.consumer.consumer import Consumer


class MockedKinesis:
    endpoint: str
    kinesis: Kinesis

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.kinesis = boto3.client('kinesis', endpoint_url=endpoint)

    def create_stream(self):
        stream_name = f'mocked-stream-{uuid.uuid4()}'
        self.kinesis.create_stream(
            StreamName=stream_name,
            ShardCount=1
        )
        return MockedStream(self.kinesis, stream_name)


class MockedStream:
    def __init__(self, kinesis: Kinesis, name: str) -> None:
        self.kinesis = kinesis
        self.name = name

    def put_record(self, data: str):
        self.kinesis.put_record(
            StreamName=self.name,
            PartitionKey=str(uuid.uuid4()),
            Data=data.encode(),
        )


MOCKED_AWS_ENV_VARS = {
    "AWS_DEFAULT_REGION": "anything",
    "AWS_ACCESS_KEY_ID": "anything",
    "AWS_SECRET_ACCESS_KEY": "anything",
}


@mock.patch.dict(os.environ, MOCKED_AWS_ENV_VARS)
def test_consume():
    mocked_kinesis = MockedKinesis('http://localhost:4567/')
    stream = mocked_kinesis.create_stream()
    stream.put_record('foo')
    stream.put_record('bar')
    stream.put_record('baz')

    consumer = Consumer()
    consumer.connect(Configuration(stream_name=stream.name, endpoint=mocked_kinesis.endpoint))

    output = StringIO()
    with redirect_stdout(output):
        consumer.consume()

    assert split_unique_lines(output.getvalue()) == {
        'foo',
        'bar',
        'baz',
    }


def split_unique_lines(getvalue: str) -> set:
    return set(getvalue.splitlines())
