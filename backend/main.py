import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles

from .api import api

app = FastAPI(
    openapi_url=None
)

app.mount("/api", api)


@app.get("/api")
async def api():
    return RedirectResponse("/api/docs")


@app.get("/")
async def api():
    return RedirectResponse("/web-compiler/")


"""
Set up for serving static asset for Angular (single page app)
"""
static_files_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
web_compiler_prefix = "/web-compiler/"


class SinglePageAppStaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404 and request.url.path.startswith(web_compiler_prefix):
            return FileResponse(os.path.join(static_files_path, "index.html"))
        return response


app.add_middleware(SinglePageAppStaticMiddleware)
app.mount(web_compiler_prefix, StaticFiles(directory=static_files_path, html=True), name="static")


@app.get("/web-compiler/")
def read_root():
    return FileResponse(os.path.join(static_files_path, "index.html"))
