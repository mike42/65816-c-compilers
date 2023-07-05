import os
import shlex
import subprocess
import tempfile
from functools import cache

from backend.compilers.wrapper_base import CompilerOutput


@cache
def compiler_exists(name: str) -> bool:
    return compiler_binary(name) != None


@cache
def compiler_binary(name: str) -> str | None:
    search_paths = os.getenv("PATH", "/bin:/usr/bin:/usr/local/bin").split(":")
    for item in search_paths:
        full_path = os.path.join(item, name)
        if os.path.exists(full_path):
            return full_path
    return None


def simple_compile(code: str, input_filename: str, command: list[str], output_filename: str,
                   absolutify: bool = False) -> CompilerOutput:
    """
    Compile <code> by writing to <filename>, running <command>, and reading assembly from <output_filename>.

    Set absolutify = True to replace the filename with an absolute path when running the command - the wdc816cc bash
    script changes directories to make WINE work.
    """
    with tempfile.TemporaryDirectory(prefix='compile-') as d:
        full_path = os.path.join(d, input_filename)
        with open(full_path, 'w') as input_file:
            input_file.write(code)
        if absolutify:
            # Set for when we want to pass an absolute path to the compiler
            command = [full_path if x == input_filename else x for x in command]
        commands = [shlex.join(command)]
        try:
            exit_code = subprocess.call(command, cwd=d)
            with open(os.path.join(d, output_filename), 'r') as output_file:
                result = output_file.read()
            return CompilerOutput(asm=result, success=exit_code == 0, commands=commands, output="")
        except Exception as e:
            return CompilerOutput(asm="; Compile was unsuccessful", success=False, commands=commands, output="")


def compile_and_disasm(code: str, input_filename: str, output_filename: str, compile_command: list[str], disasm_command: list[str]):
    """
    Compile <code> by writing to <filename>, running <compile_command> to produce a binary,
    then run disasm_command to disassemble the binary, capturing the standard output

    This process is used for ORCA/C, which doesn't have an option to produce ASM output.
    """
    with tempfile.TemporaryDirectory(prefix='compile-') as d:
        full_path = os.path.join(d, input_filename)
        with open(full_path, 'w') as input_file:
            input_file.write(code)
        # Compile step
        commands = [shlex.join(compile_command)]
        try:
            compile_output = subprocess.check_output(compile_command, cwd=d)
        except subprocess.CalledProcessError as e:
            return CompilerOutput(asm="; Compile was unsuccessful", success=False, commands=commands, output=e.output)
        if not os.path.exists(os.path.join(d, output_filename)):
            return CompilerOutput(asm="; Compile did not produce output file", success=False, commands=commands, output="")
        # Disassemble step
        commands.append(shlex.join(disasm_command))
        try:
            result = subprocess.check_output(disasm_command, cwd=d)
        except subprocess.CalledProcessError as e:
            # nonzero exit expected
            result = e.output
        return CompilerOutput(asm=result, success=True, commands=commands, output=compile_output)
