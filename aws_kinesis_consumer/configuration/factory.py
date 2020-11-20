from argparse import ArgumentParser

from aws_kinesis_consumer.configuration.configuration import Configuration


class ConfigurationFactory:
    parser: ArgumentParser

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog='aws-kinesis-consumer',
            usage='aws-kinesis-consumer --stream-name STREAM-NAME',
            description='AWS Kinesis consumer CLI. Consume records using the stream name, not the shards ids.',
        )

        self.parser.add_argument(
            '--endpoint', type=str, help="URL of the AWS Kinesis Data Stream endpoint"
        )

        required_arguments = self.parser.add_argument_group('required named arguments')
        required_arguments.add_argument(
            '--stream-name', type=str, help="Name of the Kinesis Data Stream",
            required=True
        )

    def create_configuration(self, arguments: list) -> Configuration:
        parsed = self.parser.parse_args(arguments)
        return Configuration(
            stream_name=parsed.stream_name,
            endpoint=parsed.endpoint,
        )
