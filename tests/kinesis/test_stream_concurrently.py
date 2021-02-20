import asyncio
import os
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

import pytest

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.kinesis.stream import Stream
from aws_kinesis_consumer.ui.printer import Printer
from tests.kinesis.dockerized.DockerizedKinesis import DockerizedKinesis, DUMMY_AWS_ENV_VARS

HOOK_MESSAGE = 'hook-message'


@pytest.fixture
def dockerized_kinesis() -> DockerizedKinesis:
    with mock.patch.dict(os.environ, DUMMY_AWS_ENV_VARS):
        yield DockerizedKinesis('http://localhost:4567/')


async def consume_until_getting(stream: Stream, expected_message: str, output: StringIO) -> set:
    while expected_message not in output.getvalue():
        stream.print_records()
    else:
        return split_unique_lines(output.getvalue())


def split_unique_lines(getvalue: str) -> set:
    return set(getvalue.splitlines())


@pytest.mark.asyncio
async def test_concurrently_consume(dockerized_kinesis: DockerizedKinesis):
    output = StringIO()
    with redirect_stdout(output):
        with dockerized_kinesis.create_dockerized_stream() as dockerized_stream:
            # given
            stream = Stream(AWSServicesFactory(), Printer(), Configuration(
                stream_name=dockerized_stream.name,
                region=dockerized_kinesis.region,
                endpoint=dockerized_kinesis.endpoint,
                iterator_type=IteratorType.LATEST,
                delay_in_ms=100,
                max_records_per_request=10,
            ))
            stream.prepare()

            task = asyncio.get_event_loop().create_task(
                consume_until_getting(stream, HOOK_MESSAGE, output)
            )

            dockerized_stream.put_record(HOOK_MESSAGE)

            # when
            consumed_messages: list = await task

            # then
            assert HOOK_MESSAGE in consumed_messages
