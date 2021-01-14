class ErrorHandler:

    @classmethod
    def handle(cls, error: BaseException) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        if isinstance(error, KeyboardInterrupt):
            pass
        else:
            raise error
