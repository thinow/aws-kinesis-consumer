class ErrorHandler:

    @classmethod
    def handle(cls, error: Exception) -> None:
        # User intentionally interrupts the program. Ignore the exception and exit.
        if isinstance(error, KeyboardInterrupt):
            pass
        else:
            raise error
