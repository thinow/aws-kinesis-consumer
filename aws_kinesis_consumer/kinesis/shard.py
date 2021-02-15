import time

from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorTypeProperties
from aws_kinesis_consumer.ui.printer import Printer


class Shard:
    next_shard_iterator: str

    def __init__(self, shard_id: str, configuration: Configuration, kinesis: Kinesis, printer: Printer) -> None:
        self.shard_id = shard_id
        self.configuration = configuration
        self.kinesis = kinesis
        self.printer = printer

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
            self.printer.info(f'shard iterator is null, the shard seems to be closed, shard_id={self.shard_id}')
            return

        try:
            response = self.kinesis.get_records(
                ShardIterator=self.next_shard_iterator,
                Limit=self.configuration.max_records_per_request,
            )

            records = response.get('Records')
            self.printer.info(f'shard_id={self.shard_id}, records={len(records)}')
            for record in records:
                self.printer.data(record.get('Data'))

            self.next_shard_iterator = response.get('NextShardIterator')

        except Exception as error:
            self.printer.error(f'ERROR: shard_id={self.shard_id}, message=${repr(error)}')

        finally:
            # delay recommended by AWS, see https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html
            self.wait_for_delay()

    def wait_for_delay(self):
        delay_in_mils = self.configuration.delay_in_ms
        delay_in_secs = delay_in_mils / 1_000
        time.sleep(delay_in_secs)
