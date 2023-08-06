import os
import logging
from logging.config import dictConfig
from importlib import import_module
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .core.exception_handlers import (
    custom_http_exception_handler,
    custom_request_validation_exception_handler,
)

from .core import db
from .routers import api_router
from .config.log import LogConfig


settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.dev_settings'))
app_type = import_module(os.environ.get('FASTAPI_APP_TYPE', 'dev'))

dictConfig(LogConfig().dict())
logger = logging.getLogger("app")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.1.0",
    openapi_url=f"{settings.FASTAPI_APP_PATH}/openapi.json/",
    docs_url=f"{settings.FASTAPI_APP_PATH}/docs/",
    redoc_url=f"{settings.FASTAPI_APP_PATH}/redoc/",
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await custom_http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await custom_request_validation_exception_handler(request, exc)

db.connect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix=settings.API_PATH)