from time import sleep

from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.kinesis.shard import Shard


class Stream:

    def __init__(self, name: str, shards: tuple, kinesis: Kinesis) -> None:
        self.name = name
        self.shards = shards
        self.kinesis = kinesis

    def prepare(self):
        shard: Shard
        for shard in self.shards:
            shard.prepare()

    def print_records(self):
        shard: Shard
        for shard in self.shards:
            shard.print_records()
        # TODO adapt using the config
        sleep(1)
