from botocore.exceptions import NoRegionError, NoCredentialsError, PartialCredentialsError, CredentialRetrievalError

from aws_kinesis_consumer.ui.printer import Printer


class ErrorHandler:

    def __init__(self, printer: Printer) -> None:
        self.printer = printer

    def handle(self, error: BaseException) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        if isinstance(error, KeyboardInterrupt):
            raise SystemExit(0)
        elif isinstance(error, SystemExit):
            raise SystemExit(error.code)
        elif isinstance(error, NoRegionError):
            self.printer.error('ERROR: AWS region has not been found.')
            self.printer.error('Please pass the region using the environment variable AWS_DEFAULT_REGION. Example:')
            self.printer.error('$ AWS_DEFAULT_REGION=eu-central-1 aws-kinesis-consumer --stream-name MyStream')
            raise SystemExit(1)
        elif isinstance(error, (NoCredentialsError, PartialCredentialsError, CredentialRetrievalError)):
            self.printer.error('ERROR: AWS credentials have not been found.')
            self.printer.error('Please pass the credentials using the following environment variables :')
            self.printer.error('AWS_ACCESS_KEY_ID')
            self.printer.error('AWS_SECRET_ACCESS_KEY')
            self.printer.error('AWS_SESSION_TOKEN (optional)')
            raise SystemExit(1)
        else:
            self.printer.error(f'ERROR: the program stopped due to the following issue.')
            self.printer.error(repr(error))
            raise SystemExit(1)
