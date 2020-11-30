from time import sleep

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.kinesis.shard import Shard


class Stream:
    shards: tuple

    def __init__(self, aws_services_factory: AWSServicesFactory, configuration: Configuration) -> None:
        self.aws_services_factory = aws_services_factory
        self.configuration = configuration

    def prepare(self):
        kinesis = self.aws_services_factory.create_kinesis(self.configuration)
        shards = self.create_shards(kinesis)
        [shard.prepare() for shard in shards]
        self.shards = shards

    def create_shards(self, kinesis) -> tuple:
        response = kinesis.list_shards(StreamName=self.configuration.stream_name)

        shards = map(
            lambda shard_from_response: Shard(
                shard_id=shard_from_response['ShardId'],
                configuration=self.configuration,
                kinesis=kinesis
            ),
            response['Shards']
        )

        return tuple(shards)

    def print_records(self):
        [shard.print_records() for shard in self.shards]
        self.wait_for_delay()

    def wait_for_delay(self):
        delay_in_mils = self.configuration.delay_in_ms
        delay_in_secs = delay_in_mils / 1_000
        sleep(delay_in_secs)
