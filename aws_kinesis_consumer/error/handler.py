import sys

from botocore.exceptions import NoRegionError, NoCredentialsError, PartialCredentialsError, CredentialRetrievalError


class ErrorHandler:

    @classmethod
    def handle(cls, error: BaseException) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        if isinstance(error, KeyboardInterrupt):
            raise SystemExit(0)
        elif isinstance(error, SystemExit):
            raise SystemExit(error.code)
        elif isinstance(error, NoRegionError):
            cls.print('ERROR: AWS region has not been found.')
            cls.print('Please pass the region using the environment variable AWS_DEFAULT_REGION. Example:')
            cls.print('$ AWS_DEFAULT_REGION=eu-central-1 aws-kinesis-consumer --stream-name MyStream')
            raise SystemExit(1)
        elif isinstance(error, (NoCredentialsError, PartialCredentialsError, CredentialRetrievalError)):
            cls.print('ERROR: AWS credentials have not been found.')
            cls.print('Please pass the credentials using the following environment variables :')
            cls.print('AWS_ACCESS_KEY_ID')
            cls.print('AWS_SECRET_ACCESS_KEY')
            cls.print('AWS_SESSION_TOKEN (optional)')
            raise SystemExit(1)
        else:
            cls.print(f'ERROR: the program stopped due to the following issue.')
            cls.print(repr(error))
            raise SystemExit(1)

    @classmethod
    def print(cls, text):
        print(text, file=sys.stderr)
