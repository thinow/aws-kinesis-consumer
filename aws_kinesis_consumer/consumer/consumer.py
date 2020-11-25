import boto3
from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.kinesis.shard import Shard
from aws_kinesis_consumer.kinesis.stream import Stream


class Consumer:
    stream: Stream

    def connect(self, configuration: Configuration):
        kinesis: Kinesis = boto3.client('kinesis', endpoint_url=configuration.endpoint)

        response = kinesis.list_shards(StreamName=configuration.stream_name)

        shards = tuple(map(
            lambda shard: Shard(
                shard_id=shard['ShardId'],
                configuration=configuration,
                kinesis=kinesis,
            ),
            response['Shards']
        ))

        self.stream = Stream(shards, configuration, kinesis)
        self.stream.prepare()

    def consume(self):
        self.stream.print_records()
