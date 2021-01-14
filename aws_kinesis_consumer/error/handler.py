import sys


class ErrorHandler:

    @classmethod
    def handle(cls, error: BaseException) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        # if isinstance(error, KeyboardInterrupt):
        #     pass
        print(f'ERROR: the program stopped due to the following issue.', file=sys.stderr)
        print(error, file=sys.stderr)
        sys.exit(1)
