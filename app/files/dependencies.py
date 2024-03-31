from typing import Annotated

from fastapi import Depends

from app.files.services import FilesService

from ..settings import settings
from .s3 import S3Connection


def use_s3_connection() -> S3Connection:
    conn = S3Connection(settings.s3_endpoint_url)
    return conn


def use_files_service(s3_connection: Annotated[S3Connection, Depends(use_s3_connection)]) -> FilesService:
    return FilesService(s3_connection)
