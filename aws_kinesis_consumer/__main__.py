import sys

from aws_kinesis_consumer.application import Application


def main(arguments: list):
    application = Application(arguments)
    application.prepare()
    while True:
        application.consume()
        application.wait_for_delay()


if __name__ == '__main__':
    main(sys.argv[1:])
