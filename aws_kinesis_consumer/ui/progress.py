import sys

from aws_kinesis_consumer.ui.printer import Printer


class Progress:
    def __init__(self, text: str, max_value: int, printer: Printer) -> None:
        self.current = 0
        self.goal = max_value
        self.text = text
        self.file = sys.stderr
        self.printer = printer

    def increment_and_print(self) -> None:
        self.current = self.current + 1
        self.print()

    def print(self) -> None:
        replace_line = self.current < self.goal
        self.printer.info(
            f'{self.text} {self.current}/{self.goal}',
            replaceable=replace_line
        )
