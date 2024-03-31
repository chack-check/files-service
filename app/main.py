import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .graph.router import router
from .settings import settings

logger = logging.getLogger("uvicorn.error")

logger.debug(f"Initializing sentry with dsn: {settings.sentry_dsn}")
if settings.sentry_dsn:
    sentry_sdk.init(settings.sentry_dsn)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix="/api/v1/files")
