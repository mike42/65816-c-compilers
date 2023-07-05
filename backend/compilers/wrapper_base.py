from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CompilerOutput:
    asm: str
    commands: list[str]
    output: str
    success: bool


class WrapperBase(ABC):
    @abstractmethod
    def compile(self, code: str, **kwargs) -> CompilerOutput:
        raise NotImplementedError()

    @abstractmethod
    def is_available(self) -> bool:
        return False
