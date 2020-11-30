from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorTypeProperties
from aws_kinesis_consumer.kinesis.shard import Shard


class Stream:
    shards: tuple

    def __init__(self, aws_services_factory: AWSServicesFactory, configuration: Configuration) -> None:
        self.aws_services_factory = aws_services_factory
        self.configuration = configuration

    def prepare(self):
        kinesis = self.aws_services_factory.create_kinesis(self.configuration)
        shards = self.find_shards(kinesis)
        [shard.prepare() for shard in shards]
        self.shards = shards

    def find_shards(self, kinesis) -> tuple:
        shards_ids = self.find_shards_ids(kinesis)

        shards = map(
            lambda shard_id: Shard(
                shard_id=shard_id,
                configuration=self.configuration,
                kinesis=kinesis
            ),
            shards_ids
        )

        return tuple(shards)

    def find_shards_ids(self, kinesis, next_token=None) -> list:
        iterator_type: IteratorTypeProperties = self.configuration.iterator_type.value
        if next_token is None:
            response = kinesis.list_shards(
                StreamName=self.configuration.stream_name,
                ShardFilter={
                    'Type': iterator_type.shard_filter_type
                },
            )
        else:
            response = kinesis.list_shards(
                NextToken=next_token,
            )

        shards_ids = map(
            lambda shard_response: shard_response['ShardId'],
            response['Shards']
        )

        if 'NextToken' in response:
            return list(shards_ids) + self.find_shards_ids(kinesis, response['NextToken'])
        else:
            return list(shards_ids)

    def print_records(self):
        for shard in self.shards:
            shard.print_records()
