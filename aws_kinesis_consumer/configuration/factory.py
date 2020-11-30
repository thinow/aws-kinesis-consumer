from argparse import ArgumentParser

from aws_kinesis_consumer.configuration.configuration import Configuration, IteratorType


class ConfigurationFactory:
    parser: ArgumentParser

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog='aws-kinesis-consumer',
            usage='aws-kinesis-consumer --stream-name STREAM-NAME',
            description='AWS Kinesis consumer CLI. Consume records using the stream name, not the shards ids.',
        )

        required_arguments = self.parser.add_argument_group('required named arguments')
        required_arguments.add_argument(
            '--stream-name', type=str, required=True,
            help='Name of the Kinesis Data Stream',
        )

        self.parser.add_argument(
            '--endpoint', type=str,
            help='URL of the AWS Kinesis Data Stream endpoint'
        )

        self.parser.add_argument(
            '--iterator-type', type=str, default=IteratorType.LATEST.value.argument,
            choices=[t.value.argument for t in IteratorType],
            help='''
            Shard iterator type which defines the shard position from which to start reading data records sequentially.
            "latest" gets the new records only.
            "trim-horizon" gets all the records from the beginning.
            (default: %(default)s)
            ''',
        )

    def create_configuration(self, arguments: list) -> Configuration:
        parsed = self.parser.parse_args(arguments)
        return Configuration(
            stream_name=parsed.stream_name,
            endpoint=parsed.endpoint,
            iterator_type=self.get_iterator_type(parsed.iterator_type),
            # delay recommended by AWS, see https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html
            delay_in_ms=1_000
        )

    @staticmethod
    def get_iterator_type(argument_value):
        for iterator_type in IteratorType:
            if iterator_type.value.argument == argument_value:
                return iterator_type
        else:
            raise ValueError(f'Cannot find IteratorType with argument "{argument_value}"')
