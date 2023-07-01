from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .api import api

app = FastAPI(
    openapi_url=None
)

app.mount("/api", api)


@app.get("/")
async def api():
    return RedirectResponse("/api/docs")

# TODO: Serve static files
# app.mount("/web-compiler/", StaticFiles(directory="static", html=True), name="static")
