import sys

from aws_kinesis_consumer.application.context import Context
from aws_kinesis_consumer.kinesis.stream import Stream


def main(arguments: list):
    ctx = Context()

    stream = Stream(
        ctx.aws_services_factory,
        ctx.configuration_factory.create_configuration(arguments)
    )

    stream.prepare()
    while True:
        stream.print_records()


if __name__ == '__main__':
    main(sys.argv[1:])
