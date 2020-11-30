from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.kinesis.shard import Shard
from aws_kinesis_consumer.kinesis.stream import Stream
from tests.aws.aws_services_factory import AWSServicesFactory


class Consumer:
    stream: Stream

    def __init__(self, aws_services_factory: AWSServicesFactory) -> None:
        self.aws_services_factory = aws_services_factory

    def connect(self, configuration: Configuration):
        kinesis = self.aws_services_factory.create_kinesis(configuration)

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
