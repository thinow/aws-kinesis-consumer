import sys
import time

from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorTypeProperties


class Shard:
    next_shard_iterator: str

    def __init__(self, shard_id: str, configuration: Configuration, kinesis: Kinesis) -> None:
        self.shard_id = shard_id
        self.configuration = configuration
        self.kinesis = kinesis

    def prepare(self):
        iterator_type_properties: IteratorTypeProperties = self.configuration.iterator_type.value
        iterator_response = self.kinesis.get_shard_iterator(
            ShardId=self.shard_id,
            StreamName=self.configuration.stream_name,
            ShardIteratorType=iterator_type_properties.shard_iterator_type,
        )
        self.next_shard_iterator = iterator_response.get('ShardIterator')

    def print_records(self) -> None:
        if self.next_shard_iterator is None:
            print(f'<shard iterator is null, the shard seems to be closed, shard_id={self.shard_id}>', file=sys.stderr,
                  flush=True)
            return

        try:
            response = self.kinesis.get_records(ShardIterator=self.next_shard_iterator)

            records = response.get('Records')
            print(f'<shard_id={self.shard_id}, records={len(records)}>', file=sys.stderr, flush=True)
            for record in records:
                data = record.get('Data')
                print(str(data, encoding='UTF-8'), flush=True)

            self.next_shard_iterator = response.get('NextShardIterator')

        except Exception as error:
            print(f'<error, shard_id={self.shard_id}, message={error}>', file=sys.stderr, flush=True)

        finally:
            # delay recommended by AWS, see https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html
            self.wait_for_delay()

    def wait_for_delay(self):
        delay_in_mils = self.configuration.delay_in_ms
        delay_in_secs = delay_in_mils / 1_000
        time.sleep(delay_in_secs)
