from time import sleep

import boto3
from boto3_type_annotations.kinesis import Client as KinesisClient

from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory


class Application:
    kinesis: KinesisClient
    configuration: Configuration

    def __init__(self, arguments: list) -> None:
        self.configuration = ConfigurationFactory().create_configuration(arguments)

    def prepare(self):
        self.kinesis: KinesisClient = boto3.client('kinesis', endpoint_url=self.configuration.endpoint)
        description = self.kinesis.describe_stream_summary(StreamName=self.configuration.stream_name)
        print(f'Describe stream response : {description}')

    def consume(self):
        print('<no records>')

    def wait_for_delay(self):
        # TODO adapt the time from the configuration
        sleep(1)  # in seconds
