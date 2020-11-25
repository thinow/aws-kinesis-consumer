import sys

from aws_kinesis_consumer.application.context import Context


def main(arguments: list):
    ctx = Context()

    configuration = ctx.configuration_factory.create_configuration(arguments)

    ctx.consumer.connect(configuration)
    while True:
        ctx.consumer.consume()


if __name__ == '__main__':
    main(sys.argv[1:])
