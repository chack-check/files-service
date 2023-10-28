import asyncio
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import StreamingResponse

from .s3 import S3Connection
from .schemas import FileUrl, GenerateAvatarRequest
from .dependencies import use_s3_connection
from ..auth.dependencies import auth_required
from ..settings import settings
from .avatars import avatar_generator


router = APIRouter()


@router.post("/publish", response_model=list[FileUrl], dependencies=[Depends(auth_required)])
async def publish_file(files: list[UploadFile],
                       conn: Annotated[S3Connection, Depends(use_s3_connection)]):
    coros: list[asyncio._CoroutineLike] = []
    for file in files:
        coro = conn.publish_object(settings.s3_bucket_name, file)
        coros.append(coro)

    urls = await asyncio.gather(*coros)
    return urls


@router.post("/generate", response_class=StreamingResponse)
def generate_avatar(request: GenerateAvatarRequest):
    return StreamingResponse(
        avatar_generator(request.metadata, request.title),
        media_type="image/svg+xml"
    )
