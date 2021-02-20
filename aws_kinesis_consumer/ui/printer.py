import sys


class Printer:

    def __init__(self) -> None:
        self.channel_notification = sys.stderr
        self.channel_data = sys.stdout

    def info(self, text: str, replaceable=False) -> None:
        print(
            f'> {text}',
            file=self.channel_notification,
            flush=(not replaceable),
            end=('\r' if replaceable else '\n'),
        )

    def error(self, text: str) -> None:
        print(f'! {text}', flush=True, file=self.channel_notification)

    def data(self, data_in_bytes: bytes) -> None:
        data_as_string = str(data_in_bytes, encoding='UTF-8')
        print(data_as_string, flush=True, file=self.channel_data)
