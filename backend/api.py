import os
import subprocess
import tempfile

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from backend.compilers.calypsi_6502_wrapper import Calypsi6502Wrapper
from backend.compilers.cc65_wrapper import Cc65Wrapper
from backend.util import compiler_exists
from backend.compilers.calypsi_65816_wrapper import Calypsi65816Wrapper
from backend.compilers.wdc816cc_wrapper import Wdc816ccWrapper


class CompileRequest(BaseModel):
    compiler: str
    code: str


class CompileResponse(BaseModel):
    asm: str


class CompilerSummary(BaseModel):
    id: str
    name: str
    target: str
    available: bool


api = FastAPI()


@api.get("/", include_in_schema=False)
def api_main():
    """
    Take user to the docs
    """
    return RedirectResponse("/api/docs")


@api.get("/compiler", tags=["compile"])
async def list_compilers() -> list[CompilerSummary]:
    return [
        CompilerSummary(id="cc65",
                        name="cc65 C compiler",
                        target='6502',
                        available=compiler_exists('cc65')),
        CompilerSummary(id="calypsi-65816",
                        name="Calypsi ISO C compiler for 65816",
                        target='65816',
                        available=compiler_exists('cc65816')),
        CompilerSummary(id="calypsi-6502",
                        name="Calypsi ISO C compiler for 6502",
                        target='6502',
                        available=compiler_exists('cc6502')),
        CompilerSummary(id="wdc816cc",
                        name="WDC C compiler",
                        target='65816',
                        available=compiler_exists('wdc816cc')),
        CompilerSummary(id="orca-c",
                        name="ORCA/C",
                        target='65816',
                        available=compiler_exists('iix')),
        # Not implemented.
        # CompilerSummary(id="mpw-c", name="MPW C", target='65816', available=False),
        # CompilerSummary(id="tcc816", name="TCC 65816 Port", target='65816', available=False),
    ]


@api.post("/compile", tags=["compile"])
async def do_compile(request: CompileRequest) -> CompileResponse:
    """
    Compilation process: Map to a compiler wrapper
    """
    wrapper_classes = {
        'calypsi-6502': Calypsi6502Wrapper,
        'calypsi-65816': Calypsi65816Wrapper,
        'cc65': Cc65Wrapper,
        'wdc816cc': Wdc816ccWrapper,
    }
    wrapper_class = wrapper_classes.get(request.compiler, None)
    if wrapper_class is None:
        return CompileResponse(asm="; Compiler is not supported")
    wrapper = wrapper_class()
    if not wrapper.is_available():
        return CompileResponse(asm="; Compiler is not available")
    result = wrapper.compile(request.code)
    return CompileResponse(asm=result.asm)
