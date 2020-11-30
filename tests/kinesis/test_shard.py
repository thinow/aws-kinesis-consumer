from unittest.mock import Mock

from _pytest.capture import CaptureFixture

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType
from aws_kinesis_consumer.kinesis.shard import Shard

STREAM_NAME = 'STREAM_NAME'
SHARD_ID = 'SHARD_ID'
SHARD_ITERATOR = 'SHARD_ITERATOR'
ITERATOR_TYPE = IteratorType.LATEST


def test_prepare_should_fetch_shard_iterator():
    # given
    shard, kinesis = create_shard()

    # when
    shard.prepare()

    # then
    kinesis.get_shard_iterator.assert_called_with(
        ShardId=SHARD_ID,
        StreamName=STREAM_NAME,
        ShardIteratorType=ITERATOR_TYPE.name,
    )


def test_print_records(capsys: CaptureFixture):
    # given
    shard, kinesis = create_shard()

    kinesis.get_records.return_value = {'Records': [
        {'Data': bytes('RECORD-1', 'UTF-8')},
        {'Data': bytes('RECORD-2', 'UTF-8')},
    ]}

    # when
    shard.prepare()
    shard.print_records()

    # then
    kinesis.get_records.assert_called_with(ShardIterator=SHARD_ITERATOR)
    assert capsys.readouterr().out.splitlines() == [
        'RECORD-1',
        'RECORD-2',
    ]


def test_print_records_when_no_records(capsys: CaptureFixture):
    # given
    shard, kinesis = create_shard()

    kinesis.get_records.return_value = {'Records': []}

    # when
    shard.prepare()
    shard.print_records()

    # then
    assert capsys.readouterr().err.splitlines() == [
        '<no records, shard_id=SHARD_ID>'
    ]


def test_print_records_use_next_shard_iterator():
    # given
    shard, kinesis = create_shard()

    kinesis.get_records.return_value = {'Records': [], 'NextShardIterator': 'NEXT-SHARD-ITERATOR'}

    # when
    shard.prepare()
    for index in range(2):
        shard.print_records()

    # then
    kinesis.get_records.assert_called_with(ShardIterator='NEXT-SHARD-ITERATOR')


def test_print_records_when_next_shard_iterator_is_none(capsys: CaptureFixture):
    # given
    shard, kinesis = create_shard()

    kinesis.get_records.return_value = {'Records': [], 'NextShardIterator': None}

    # when
    shard.prepare()
    for index in range(2):
        shard.print_records()

    # then
    assert capsys.readouterr().err.splitlines() == [
        '<no records, shard_id=SHARD_ID>',
        '<shard iterator is null, the shard seems to be closed, shard_id=SHARD_ID>',
    ]


def test_print_records_on_error(capsys: CaptureFixture):
    # given
    shard, kinesis = create_shard()

    kinesis.get_records.side_effect = RuntimeError('TEST-ERROR')

    # when
    shard.prepare()
    shard.print_records()

    # then
    assert capsys.readouterr().out == ''


def create_shard():
    kinesis = Mock()
    kinesis.get_shard_iterator.return_value = {'ShardIterator': SHARD_ITERATOR}

    configuration = Configuration(STREAM_NAME, ITERATOR_TYPE, None, 0)
    shard = Shard(SHARD_ID, configuration, kinesis)

    return shard, kinesis
