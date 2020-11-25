from time import sleep

from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.kinesis.shard import Shard


class Stream:

    def __init__(self, shards: tuple, configuration: Configuration, kinesis: Kinesis) -> None:
        self.shards = shards
        self.configuration = configuration
        self.kinesis = kinesis

    def prepare(self):
        shard: Shard
        for shard in self.shards:
            shard.prepare()

    def print_records(self):
        shard: Shard
        for shard in self.shards:
            shard.print_records()

        delay_in_secs = self.configuration.delay_in_ms / 1_000
        sleep(delay_in_secs)
