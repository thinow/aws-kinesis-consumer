import os
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

import pytest

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.consumer.consumer import Consumer
from tests.consumer.MockedKinesis import MockedKinesis

MOCKED_AWS_ENV_VARS = {
    "AWS_DEFAULT_REGION": "anything",
    "AWS_ACCESS_KEY_ID": "anything",
    "AWS_SECRET_ACCESS_KEY": "anything",
}


@pytest.fixture
def mocked_kinesis() -> MockedKinesis:
    with mock.patch.dict(os.environ, MOCKED_AWS_ENV_VARS):
        yield MockedKinesis('http://localhost:4567/')


def test_consume(mocked_kinesis: MockedKinesis):
    stream = mocked_kinesis.create_stream()
    stream.put_record('foo')
    stream.put_record('bar')
    stream.put_record('baz')

    consumer = Consumer()
    consumer.connect(Configuration(
        stream_name=stream.name,
        endpoint=mocked_kinesis.endpoint,
        iterator_type=IteratorType.TRIM_HORIZON,
        delay_in_ms=0
    ))

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
