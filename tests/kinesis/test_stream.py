import os
from unittest import mock

import pytest
from _pytest.capture import CaptureFixture

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.kinesis.stream import Stream
from tests.consumer.DockerizedKinesis import DockerizedKinesis

DUMMY_AWS_ENV_VARS = {
    "AWS_DEFAULT_REGION": "anything",
    "AWS_ACCESS_KEY_ID": "anything",
    "AWS_SECRET_ACCESS_KEY": "anything",
}


@pytest.fixture
def dockerized_kinesis() -> DockerizedKinesis:
    with mock.patch.dict(os.environ, DUMMY_AWS_ENV_VARS):
        yield DockerizedKinesis('http://localhost:4567/')


def test_consume(dockerized_kinesis: DockerizedKinesis, capsys: CaptureFixture):
    # given
    dockerized_stream = dockerized_kinesis.create_dockerized_stream()
    dockerized_stream.put_record('foo')
    dockerized_stream.put_record('bar')
    dockerized_stream.put_record('baz')

    stream_helper = Stream(AWSServicesFactory(), Configuration(
        stream_name=dockerized_stream.name,
        endpoint=dockerized_kinesis.endpoint,
        iterator_type=IteratorType.TRIM_HORIZON,
        delay_in_ms=0
    ))

    # when
    stream_helper.prepare()
    stream_helper.print_records()

    # then
    assert split_unique_lines(capsys.readouterr().out) == {
        'foo',
        'bar',
        'baz',
    }


def split_unique_lines(getvalue: str) -> set:
    return set(getvalue.splitlines())
