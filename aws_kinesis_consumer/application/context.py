from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory


class Context:

    def __init__(self) -> None:
        self.configuration_factory = ConfigurationFactory()
        self.aws_services_factory = AWSServicesFactory()
