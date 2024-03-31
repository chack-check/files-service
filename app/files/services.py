from tempfile import NamedTemporaryFile

import cv2
from fastapi import UploadFile

from app.files.exceptions import FileValidationError, FileWithoutFilenameError
from app.files.s3 import S3Connection
from app.files.schemas import ConvertionOptions, SavedFile, SystemFiletypes
from app.files.utils import get_media_type_for_filename
from app.settings import settings

from .savers import GenericSaver, PhotoSaver


class FilesValidator:

    def validate_avatar(self, file: UploadFile):
        if not file.filename:
            raise FileWithoutFilenameError()

        media_type = get_media_type_for_filename(file.filename)
        if media_type == "video":
            self._validate_video_duration(file, 10)

    def _validate_video_duration(self, file: UploadFile, max_duration: int) -> None:
        named_file = NamedTemporaryFile("w+b")
        named_file.write(file.file.read())
        named_file.seek(0)
        cap = cv2.VideoCapture(named_file.name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        named_file.close()
        duration = frame_count / fps
        if duration > settings.max_avatar_video_duration:
            raise FileValidationError(f"Max avatar video duration is: {settings.max_avatar_video_duration}")

    def validate_file_in_chat(self, file: UploadFile):
        ...

    def validate_file(self, file: UploadFile, system_type: SystemFiletypes) -> None:
        match system_type:
            case SystemFiletypes.avatar:
                self.validate_avatar(file)
            case SystemFiletypes.file_in_chat:
                self.validate_file_in_chat(file)


class FilesService:

    def __init__(self, s3_connection: S3Connection) -> None:
        self.photo_saver = PhotoSaver(s3_connection)
        self.generic_saver = GenericSaver(s3_connection)
        self.validator = FilesValidator()

    async def save_file(self, file: UploadFile,
                        system_filetype: SystemFiletypes,
                        convert_to: ConvertionOptions | None = None,
                        compress: bool = True) -> SavedFile:
        self.validator.validate_file(file, system_filetype)
        if not file.filename:
            raise FileWithoutFilenameError

        media_type = get_media_type_for_filename(file.filename)
        match media_type:
            case "image":
                return await self.photo_saver.save_file(
                    file,
                    system_filetype.value,
                    convert_to.value if convert_to else None,
                    compress
                )
            # case "video":
            #     self._save_video_file(file, system_filetype, convert_to, compress)
            # case "audio":
            #     self._save_audio_file(file, system_filetype, convert_to, compress)
            case _:
                return await self.generic_saver.save_file(file, system_filetype.value)
