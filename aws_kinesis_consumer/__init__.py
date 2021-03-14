import sys

from aws_kinesis_consumer.aws.aws_services_factory import AWSServicesFactory
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory
from aws_kinesis_consumer.error.handler import ErrorHandler
from aws_kinesis_consumer.kinesis.stream import Stream
from aws_kinesis_consumer.ui.printer import Printer


def main():
    arguments = sys.argv[1:]

    printer = Printer()
    configuration = None

    try:
        configuration = ConfigurationFactory().create_configuration(arguments)

        stream = Stream(
            aws_services_factory=AWSServicesFactory(),
            printer=printer,
            configuration=configuration,
        )

        stream.prepare()
        while True:
            stream.print_records()

    except BaseException as error:
        ErrorHandler(printer, configuration).handle(error)
