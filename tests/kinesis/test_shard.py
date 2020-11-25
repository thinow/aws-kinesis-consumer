from unittest.mock import Mock

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.kinesis.shard import Shard


def test_prepare_should_fetch_shard_iterator():
    # given
    kinesis = Mock()
    kinesis.get_shard_iterator.return_value = {'ShardIterator': 'SHARD_ITERATOR'}

    configuration = Configuration('STREAM_NAME', IteratorType.LATEST)
    shard = Shard('SHARD_ID', configuration, kinesis)

    # when
    shard.prepare()

    # then
    kinesis.get_shard_iterator.assert_called_with(
        ShardId='SHARD_ID',
        StreamName='STREAM_NAME',
        ShardIteratorType='LATEST',
    )
