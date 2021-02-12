import sys


class Printer:

    def __init__(self) -> None:
        self.flush = True
        self.data_encoding = 'UTF-8'

    def info(self, text: str) -> None:
        # TODO change the format for "# TEXT" ?
        print(f'<{text}>', flush=self.flush, file=sys.stderr)

    def error(self, text: str, error: BaseException) -> None:
        self.info(f'ERROR : {text}, message={repr(error)}')

    def print_data(self, data: bytes) -> None:
        data_as_string = str(data, encoding=self.data_encoding)
        print(data_as_string, flush=self.flush, file=sys.stdout)
