import os
from unittest import mock
from unittest.mock import Mock, call

import pytest
from _pytest.capture import CaptureFixture
from boto3_type_annotations.kinesis import Client

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.kinesis.stream import Stream
from aws_kinesis_consumer.ui.printer import Printer
from tests.kinesis.dockerized.DockerizedKinesis import DUMMY_AWS_ENV_VARS
from tests.kinesis.dockerized.DockerizedKinesis import DockerizedKinesis


@pytest.fixture
def dockerized_kinesis() -> DockerizedKinesis:
    with mock.patch.dict(os.environ, DUMMY_AWS_ENV_VARS):
        yield DockerizedKinesis('http://localhost:4567/')


def test_consume(dockerized_kinesis: DockerizedKinesis, capsys: CaptureFixture):
    with dockerized_kinesis.create_dockerized_stream() as dockerized_stream:
        # given
        dockerized_stream.put_record('foo')
        dockerized_stream.put_record('bar')
        dockerized_stream.put_record('baz')

        stream_helper = Stream(AWSServicesFactory(), Printer(), Configuration(
            stream_name=dockerized_stream.name,
            region=dockerized_kinesis.region,
            endpoint=dockerized_kinesis.endpoint,
            iterator_type=IteratorType.TRIM_HORIZON,
            delay_in_ms=0,
            max_records_per_request=10,
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


def test_prepare_should_list_shards():
    # given
    stream, kinesis = create_stream_with_mocks(Configuration(
        stream_name='any-stream-name',
        iterator_type=IteratorType.LATEST,
        endpoint=None,
        delay_in_ms=0,
        max_records_per_request=10,
    ))

    kinesis.list_shards.return_value = {
        'Shards': [
            {'ShardId': 'shard-id-001'},
            {'ShardId': 'shard-id-002'},
        ]
    }

    # when
    stream.prepare()

    # then
    assert list(map(lambda s: s.shard_id, stream.shards)) == [
        'shard-id-001',
        'shard-id-002',
    ]


def test_prepare_should_filter_shards_based_on_iterator():
    # given
    stream, kinesis = create_stream_with_mocks(Configuration(
        stream_name='any-stream-name',
        iterator_type=IteratorType.TRIM_HORIZON,
        endpoint=None,
        delay_in_ms=0,
        max_records_per_request=10,
    ))

    # when
    stream.prepare()

    # then
    kinesis.list_shards.assert_called_with(
        StreamName='any-stream-name',
        ShardFilter={
            'Type': 'AT_TRIM_HORIZON'
        }
    )


def test_prepare_should_list_subsequent_shards():
    # given
    stream, kinesis = create_stream_with_mocks(Configuration(
        stream_name='any-stream-name',
        iterator_type=IteratorType.LATEST,
        endpoint=None,
        delay_in_ms=0,
        max_records_per_request=10,
    ))

    kinesis.list_shards.side_effect = [
        {'Shards': [{'ShardId': 'shard-id-001'}], 'NextToken': 'any', },
        {'Shards': [{'ShardId': 'shard-id-002'}], 'NextToken': 'any', },
        {'Shards': [{'ShardId': 'shard-id-003'}], },
    ]

    # when
    stream.prepare()

    # then
    assert list(map(lambda s: s.shard_id, stream.shards)) == [
        'shard-id-001',
        'shard-id-002',
        'shard-id-003',
    ]


def test_prepare_should_list_using_tokens():
    # given
    stream, kinesis = create_stream_with_mocks(Configuration(
        stream_name='any-stream-name',
        iterator_type=IteratorType.LATEST,
        endpoint=None,
        delay_in_ms=0,
        max_records_per_request=10,
    ))

    kinesis.list_shards.side_effect = [
        {'Shards': [], 'NextToken': 'first-test-token', },
        {'Shards': [], 'NextToken': 'second-test-token', },
        {'Shards': [], },
    ]

    # when
    stream.prepare()

    # then
    assert kinesis.list_shards.call_args_list == [
        call(StreamName='any-stream-name', ShardFilter={'Type': 'AT_LATEST'}),
        call(NextToken='first-test-token'),
        call(NextToken='second-test-token'),
    ]


def create_stream_with_mocks(configuration: Configuration):
    kinesis: Client = Mock()
    kinesis.list_shards.return_value = {
        'Shards': []
    }

    aws_services_factory: AWSServicesFactory = Mock()
    aws_services_factory.create_kinesis.return_value = kinesis

    stream = Stream(aws_services_factory, Printer(), configuration)

    return stream, kinesis
