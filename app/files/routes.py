from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

from app.files.exceptions import FileValidationError

from ..auth.dependencies import auth_required
from .dependencies import use_files_service
from .exceptions import CantConvertFile, FileWithoutFilenameError, IncorrectMIMEType
from .schemas import ConvertionOptions, SavedFile, SystemFiletypes
from .services import FilesService

router = APIRouter()


@router.post("/publish", response_model=list[SavedFile], dependencies=[Depends(auth_required)])
async def publish_file(files: list[UploadFile],
                       system_filetype: Annotated[SystemFiletypes, Form(...)],
                       compress: Annotated[bool, Form(...)],
                       files_service: Annotated[FilesService, Depends(use_files_service)],
                       convert_to: Annotated[ConvertionOptions | None, Form()] = None):
    urls = []
    for file in files:
        try:
            saved_file = await files_service.save_file(
                file,
                system_filetype,
                convert_to if convert_to else None,
                compress
            )
            urls.append(saved_file)
        except (FileValidationError, FileWithoutFilenameError, CantConvertFile, IncorrectMIMEType) as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])

    return urls
