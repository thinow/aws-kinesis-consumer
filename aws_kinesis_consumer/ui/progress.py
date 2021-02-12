import sys


class Progress:
    def __init__(self, text: str, max_value: int) -> None:
        self.progress = 0
        self.goal = max_value
        self.text = text
        self.file = sys.stderr

    def increment_and_print(self):
        self.progress = self.progress + 1
        self.print()

    def print(self) -> None:
        replace_line = self.progress < self.goal
        if replace_line:
            print(self.get_printable(), file=self.file, flush=False, end='\r')
        else:
            print(self.get_printable(), file=self.file, flush=True)

    def get_printable(self) -> str:
        return f'<{self.text} {self.progress}/{self.goal}>'
