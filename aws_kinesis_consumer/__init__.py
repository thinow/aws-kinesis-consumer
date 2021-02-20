import sys

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory
from aws_kinesis_consumer.error.handler import ErrorHandler
from aws_kinesis_consumer.kinesis.stream import Stream
from aws_kinesis_consumer.ui.printer import Printer


def main():
    arguments = sys.argv[1:]

    printer = Printer()

    try:
        configuration_factory = ConfigurationFactory()
        aws_services_factory = AWSServicesFactory()

        stream = Stream(
            aws_services_factory=aws_services_factory,
            printer=printer,
            configuration=configuration_factory.create_configuration(arguments),
        )

        stream.prepare()
        while True:
            stream.print_records()

    except BaseException as error:
        ErrorHandler(printer).handle(error)
