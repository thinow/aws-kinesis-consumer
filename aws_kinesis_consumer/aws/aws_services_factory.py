import boto3
from boto3_type_annotations.kinesis import Client as Kinesis

from aws_kinesis_consumer.configuration.configuration import Configuration


class AWSServicesFactory:

    def create_kinesis(self, configuration: Configuration) -> Kinesis:
        return boto3.client(
            'kinesis',
            endpoint_url=configuration.endpoint,
            region_name=configuration.region,
        )
