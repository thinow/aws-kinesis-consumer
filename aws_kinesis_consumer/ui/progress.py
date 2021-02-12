import sys


class Progress:
    def __init__(self, text: str, max_value: int) -> None:
        self.current = 0
        self.goal = max_value
        self.text = text
        self.file = sys.stderr

    def increment_and_print(self):
        self.current = self.current + 1
        self.print()

    def print(self) -> None:
        replace_line = self.current < self.goal
        if replace_line:
            print(self.get_printable(), file=self.file, flush=False, end='\r')
        else:
            print(self.get_printable(), file=self.file, flush=True)

    def get_printable(self) -> str:
        return f'<{self.text} {self.current}/{self.goal}>'
