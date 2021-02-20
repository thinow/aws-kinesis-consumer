from botocore.exceptions import NoRegionError, NoCredentialsError, PartialCredentialsError, CredentialRetrievalError, \
    ClientError

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
            self.printer.error('Please pass the region using the --region argument. Example:')
            self.printer.error('$ aws-kinesis-consumer --stream-name MyStream --region us-east-1')
            raise SystemExit(1)
        elif isinstance(error, (NoCredentialsError, PartialCredentialsError, CredentialRetrievalError)):
            self.printer.error('ERROR: AWS credentials have not been found.')
            self.printer.error('Please pass the credentials using the following environment variables :')
            self.printer.error('AWS_ACCESS_KEY_ID')
            self.printer.error('AWS_SECRET_ACCESS_KEY')
            self.printer.error('AWS_SESSION_TOKEN (optional)')
            raise SystemExit(1)
        elif ErrorHandler.is_client_error_with_code(error, 'ExpiredTokenException'):
            self.printer.error('ERROR: AWS session token has expired.')
            self.printer.error('Please refresh the AWS credentials.')
            raise SystemExit(1)
        elif ErrorHandler.is_client_error_with_code(error, 'ResourceNotFoundException'):
            self.printer.error('ERROR: the Kinesis Stream has not been found.')
            self.printer.error(error.response.get('Error', {}).get('Message', 'Unknown'))
            self.printer.error('Hint: verify the account id, the stream name, and the AWS region.')
            raise SystemExit(1)
        else:
            self.printer.error(f'ERROR: the program stopped due to the following issue.')
            self.printer.error(repr(error))
            raise SystemExit(1)

    @staticmethod
    def is_client_error_with_code(error: BaseException, error_code: str) -> bool:
        if not isinstance(error, ClientError):
            return False

        if 'Error' not in error.response:
            return False

        if 'Code' not in error.response['Error']:
            return False

        return error.response['Error']['Code'] == error_code
