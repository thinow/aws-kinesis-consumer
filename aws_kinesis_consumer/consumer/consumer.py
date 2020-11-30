from aws_kinesis_consumer.configuration.configuration import Configuration
from aws_kinesis_consumer.kinesis.stream import Stream
from tests.aws.aws_services_factory import AWSServicesFactory


class Consumer:
    stream: Stream

    def __init__(self, aws_services_factory: AWSServicesFactory) -> None:
        self.aws_services_factory = aws_services_factory

    def connect(self, configuration: Configuration):
        self.stream = Stream(self.aws_services_factory, configuration)
        self.stream.prepare()

    def consume(self):
        self.stream.print_records()
