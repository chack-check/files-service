from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .graph.router import router
from .settings import settings

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix="/api/v1/files")
