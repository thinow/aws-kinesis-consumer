import sys

from boto3_type_annotations.kinesis import Client as Kinesis


class Shard:
    next_shard_iterator: str

    def __init__(self, stream_name: str, shard_id: str, kinesis: Kinesis) -> None:
        self.stream_name = stream_name
        self.shard_id = shard_id
        self.kinesis = kinesis

    def prepare(self):
        # TODO handle errors
        iterator_response = self.kinesis.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=self.shard_id,
            ShardIteratorType='TRIM_HORIZON',
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
