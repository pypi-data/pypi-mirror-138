
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .api import routes as api


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.get("/ping", response_class=HTMLResponse)
async def root(request: Request):
    return 'pong'

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("pystringbio.server:app", host="127.0.0.1", port=8000, reload=True)

