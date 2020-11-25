from aws_kinesis_consumer.configuration.factory import ConfigurationFactory
from aws_kinesis_consumer.consumer.consumer import Consumer


class Context:

    def __init__(self) -> None:
        self.configuration_factory = ConfigurationFactory()
        self.consumer = Consumer()
