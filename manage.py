# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Fastapi celery example."""
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from initializer import IncludeAPIRouter
from fastapi.staticfiles import StaticFiles
from config import settings
app = FastAPI()

def get_application():
    _app = FastAPI(title="Fast API🚀",
                   description="AIP490-BE",
                   version="0.0.1")
    _app.include_router(IncludeAPIRouter())

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app

app = get_application()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

if __name__ == "__main__":
    uvicorn.run("manage:app",
                host='127.0.0.1', 
                port=8000, 
                use_colors=True,
                reload=True)
