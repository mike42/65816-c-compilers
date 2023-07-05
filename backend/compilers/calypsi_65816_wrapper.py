from backend.compilers.wrapper_base import WrapperBase, CompilerOutput
from backend.util import compiler_exists, simple_compile


class Calypsi65816Wrapper(WrapperBase):
    def compile(self, code: str, **kwargs) -> CompilerOutput:
        return simple_compile(code=code,
                              input_filename='code.c',
                              command=["cc65816", "-S", "code.c"],
                              output_filename="code.s")

    def is_available(self) -> bool:
        return compiler_exists("cc65816")
