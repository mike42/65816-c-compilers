import os
import subprocess
import tempfile

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from backend.util import compiler_exists


class CompileRequest(BaseModel):
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
    Compilation process
    """
    with tempfile.TemporaryDirectory(prefix='compile-') as d:
        try:
            with open(os.path.join(d, 'code.c'), 'w') as input_file:
                input_file.write(request.code)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        try:
            # exit_code = subprocess.call(["wdc816cc", "-MS", "-A", "code.c"], cwd=d)
            exit_code = subprocess.call(["cc65816", "-S", "code.c"], cwd=d)
            with open(os.path.join(d, 'code.s'), 'r') as output_file:
                result = output_file.read()
            # with open(os.path.join(d, 'code.asm'), 'r') as output_file:
            #     result = output_file.read()
            return CompileResponse(asm=result)
        except Exception as e:
            return CompileResponse(asm="; Compile was unsuccessful \n;" + "\n; ".join(request.code.split("\n")))
