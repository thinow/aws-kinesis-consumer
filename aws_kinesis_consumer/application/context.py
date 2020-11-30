from aws_kinesis_consumer.configuration.factory import ConfigurationFactory
from aws_kinesis_consumer.consumer.consumer import Consumer
from tests.aws.aws_services_factory import AWSServicesFactory


class Context:

    def __init__(self) -> None:
        self.configuration_factory = ConfigurationFactory()
        self.aws_services_factory = AWSServicesFactory()
        self.consumer = Consumer(self.aws_services_factory)
