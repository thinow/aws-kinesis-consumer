import sys


# TODO unit test

class Printer:

    def __init__(self) -> None:
        self.data_encoding = 'UTF-8'

    def info(self, text: str, replaceable=False) -> None:
        print(
            # TODO change the format for "# TEXT" ?
            f'<{text}>',
            file=sys.stderr,
            flush=(not replaceable),
            end=('\r' if replaceable else '\n'),
        )

    def error(self, text: str, error: BaseException) -> None:
        self.info(f'ERROR : {text}, message={repr(error)}')

    def print_data(self, data: bytes) -> None:
        data_as_string = str(data, encoding=self.data_encoding)
        print(data_as_string, flush=True, file=sys.stdout)
