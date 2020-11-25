import sys

from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration


class Shard:
    next_shard_iterator: str

    def __init__(self, shard_id: str, configuration: Configuration, kinesis: Kinesis) -> None:
        self.shard_id = shard_id
        self.configuration = configuration
        self.kinesis = kinesis

    def prepare(self):
        # TODO handle errors
        iterator_response = self.kinesis.get_shard_iterator(
            ShardId=self.shard_id,
            StreamName=self.configuration.stream_name,
            ShardIteratorType=self.configuration.iterator_type.name,
        )
        self.next_shard_iterator = iterator_response.get('ShardIterator')

    def print_records(self) -> None:
        # TODO handle errors
        # TODO handle None iterator
        records = self.kinesis.get_records(ShardIterator=self.next_shard_iterator)

        for record in records.get('Records'):
            data = record.get('Data')
            print(str(data, encoding='UTF-8'))

        else:
            print(f'<no records, shard_id = {self.shard_id}>', file=sys.stderr)

        # TODO handle None NextShardIterator (shard should not be consumed anymore)
        self.next_shard_iterator = records.get('NextShardIterator')
