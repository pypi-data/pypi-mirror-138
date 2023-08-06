from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import os


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

# Mounting default Vue files after running npm run build 
#app.mount("/dist", StaticFiles(directory="client/dist/"), name="dist")
#app.mount("/css", StaticFiles(directory="client/dist/css"), name="css")
#app.mount("/img", StaticFiles(directory="client/dist/img"), name="img")
#app.mount("/js", StaticFiles(directory="client/dist/js"), name="js")
#templates = Jinja2Templates(directory="client/dist")

@app.get("/ping", response_class=HTMLResponse)
async def root(request: Request):
    return 'pong'
    #return templates.TemplateResponse("index.html", {"request": request})
