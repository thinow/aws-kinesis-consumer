import sys

from botocore.exceptions import NoRegionError


class ErrorHandler:

    @classmethod
    def handle(cls, error: BaseException) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        if isinstance(error, KeyboardInterrupt):
            pass
        elif isinstance(error, NoRegionError):
            print('ERROR: AWS region has not been found.', file=sys.stderr)
            print('Please pass the region using the environment variable AWS_DEFAULT_REGION. Example:', file=sys.stderr)
            print('$ AWS_DEFAULT_REGION=eu-central-1 aws-kinesis-consumer --stream-name MyStream', file=sys.stderr)
            sys.exit(1)
        else:
            print(f'ERROR: the program stopped due to the following issue.', file=sys.stderr)
            print(repr(error), file=sys.stderr)
            sys.exit(1)
