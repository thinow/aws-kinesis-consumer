import os
from unittest import mock

import pytest
from _pytest.capture import CaptureFixture

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.consumer.consumer import Consumer
from tests.aws.aws_services_factory import AWSServicesFactory
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


def test_consume(mocked_kinesis: MockedKinesis, capsys: CaptureFixture):
    # given
    stream = mocked_kinesis.create_stream()
    stream.put_record('foo')
    stream.put_record('bar')
    stream.put_record('baz')

    consumer = Consumer(AWSServicesFactory())
    consumer.connect(Configuration(
        stream_name=stream.name,
        endpoint=mocked_kinesis.endpoint,
        iterator_type=IteratorType.TRIM_HORIZON,
        delay_in_ms=0
    ))

    # when
    consumer.consume()

    # then
    assert split_unique_lines(capsys.readouterr().out) == {
        'foo',
        'bar',
        'baz',
    }


def split_unique_lines(getvalue: str) -> set:
    return set(getvalue.splitlines())
