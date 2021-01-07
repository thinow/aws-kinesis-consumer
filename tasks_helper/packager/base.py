from abc import ABC, abstractmethod

import invoke


class Packager(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def build(self, runner: invoke.Runner) -> None:
        pass
