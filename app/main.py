from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .files.routes import router as files_router
from .settings import settings


app = FastAPI(
    docs_url="/api/v1/files/docs" if settings.run_mode == 'dev' else None,
    redoc_url="/api/v1/files/redoc" if settings.run_mode == 'dev' else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(files_router, prefix="/api/v1/files")
