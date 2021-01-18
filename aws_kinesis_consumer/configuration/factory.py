from argparse import ArgumentParser

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType

AWS_KINESIS_CONSUMER_VERSION = "1.1.1"


class ConfigurationFactory:
    parser: ArgumentParser

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog='aws-kinesis-consumer',
            usage='aws-kinesis-consumer --stream-name STREAM-NAME',
            description='''
                Consume an AWS Kinesis Data Stream to look over the records from a terminal.
                See https://aws.amazon.com/kinesis/data-streams/
            ''',
        )

        required_arguments = self.parser.add_argument_group('required named arguments')
        required_arguments.add_argument(
            '--stream-name', type=str, required=True,
            help='define the name of the Kinesis Data Stream which will be consumed',
        )

        self.parser.add_argument(
            '--endpoint', type=str,
            help='''
                define an URL of the AWS Kinesis Data Stream endpoint different from the default AWS endpoint
                (e.g. https://kinesis.us-east-1.amazonaws.com/)
            '''
        )

        self.parser.add_argument(
            '--iterator-type', type=str, default=IteratorType.LATEST.value.argument,
            choices=[t.value.argument for t in IteratorType],
            help='''
            define the position in the shard from where to start reading data records.
            "latest" to start from the latest records (e.g. the freshly produced records only).
            "trim-horizon" to start from the earliest records (e.g. all records existing in the shards, then the freshly
            produced records).
            (default: %(default)s)
            ''',
        )

        self.parser.add_argument(
            '--version',
            action='version',
            version=AWS_KINESIS_CONSUMER_VERSION
        )

    def create_configuration(self, arguments: list) -> Configuration:
        parsed = self.parser.parse_args(arguments)
        return Configuration(
            stream_name=parsed.stream_name,
            endpoint=parsed.endpoint,
            iterator_type=self.get_iterator_type(parsed.iterator_type),
            # delay recommended by AWS, see https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html
            delay_in_ms=1_000,
            max_records_per_request=10,  # TODO pick up from arguments
        )

    @staticmethod
    def get_iterator_type(argument_value):
        for iterator_type in IteratorType:
            if iterator_type.value.argument == argument_value:
                return iterator_type
        else:
            raise ValueError(f'Cannot find IteratorType with argument "{argument_value}"')
