from abc import ABC, abstractmethod

import invoke


class Packager(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def build(self, runner: invoke.Runner) -> None:
        pass

    @abstractmethod
    def deploy(self, runner: invoke.Runner, destination: str) -> None:
        pass
