import os
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import tempfile


class CompileRequest(BaseModel):
    code: str


class CompileResponse(BaseModel):
    asm: str


api = FastAPI()


@api.get("/", include_in_schema=False)
def api_main():
    """
    Take user to the docs
    """
    return RedirectResponse("/api/docs")


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
