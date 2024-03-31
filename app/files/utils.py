import hashlib
import hmac
import mimetypes

from fastapi import HTTPException, status

from app.settings import settings

from .exceptions import FileValidationError, IncorrectMIMEType


def generate_signature(filename: str, system_filetype: str) -> str:
    encoding_bytes = (f"{filename}:{system_filetype}").encode()
    return hmac.new(settings.signature_key.encode(), encoding_bytes, hashlib.sha256).hexdigest()


def get_media_type_for_filename(filename: str) -> str:
    mimetypes.init()
    mimestart = mimetypes.guess_type(filename)[0]
    media_type = mimestart.split('/')[0] if mimestart else None
    if not media_type:
        raise IncorrectMIMEType(filename)

    return media_type


def handle_file_validation_error(coro):

    async def wrap():
        try:
            return await coro
        except FileValidationError as e:
            HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])

    return wrap()
