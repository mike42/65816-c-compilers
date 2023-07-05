from backend.compilers.wrapper_base import WrapperBase, CompilerOutput
from backend.util import compiler_exists, simple_compile


class Wdc816ccWrapper(WrapperBase):
    def compile(self, code: str, **kwargs) -> CompilerOutput:
        return simple_compile(code=code,
                              input_filename='code.c',
                              command=["wdc816cc", "-MS", "-A", "code.c"],
                              output_filename="code.asm",
                              absolutify=True)

    def is_available(self) -> bool:
        return compiler_exists("cc65")
