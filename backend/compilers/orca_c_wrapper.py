from backend.compilers.wrapper_base import WrapperBase, CompilerOutput
from backend.util import compiler_exists, compile_and_disasm


class OrcaCWrapper(WrapperBase):
    def compile(self, code: str, **kwargs) -> CompilerOutput:
        return compile_and_disasm(
            code=code,
            input_filename='code.cc',
            output_filename="code.a",
            compile_command=["iix", "compile", "code.cc"],
            disasm_command=["iix", "dumpobj", "+D", "-S", "code.a"],
        )

    def is_available(self) -> bool:
        return compiler_exists("iix")
