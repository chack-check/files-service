import io

from fastapi import UploadFile

from app.files.constants import NOT_CONVERTABLE_EXTENSIONS
from app.files.exceptions import CantConvertFile, FileWithoutFilenameError
from app.files.s3 import S3Connection
from app.files.schemas import FileUrl, FileUrlWithSignature, SavedFile, SystemFiletypes
from app.files.utils import generate_signature
from app.settings import settings

from .converters import (
    BaseConverter,
    ImageJpgConverter,
    ImagePngConverter,
    ImageWebpConverter,
)


class BaseSaver:
    converters: dict[str, BaseConverter]

    def __init__(self, s3_connection: S3Connection):
        self._s3_connection = s3_connection

    def _get_converted_file_extension(self, file: UploadFile, convert_to: str | None = None) -> str | None:
        if not file.filename:
            raise FileWithoutFilenameError()

        file_extension = convert_to if convert_to else file.filename.split('.')[-1]
        if file_extension not in self.converters:
            return None

        return file_extension

    def _is_file_extension_not_convertable(self, filename: str) -> bool:
        file_extension = filename.split('.')[-1]
        if file_extension in NOT_CONVERTABLE_EXTENSIONS:
            return True

        return False

    def _get_converter_by_filename(self, file: UploadFile, convert_to: str | None = None) -> BaseConverter | None:
        if not file.filename:
            raise FileWithoutFilenameError()

        if self._is_file_extension_not_convertable(file.filename):
            return None

        file_extension = self._get_converted_file_extension(file, convert_to)
        if not file_extension:
            return None

        return self.converters[file_extension]

    def _get_new_file_filename(self, file: UploadFile, convert_to: str | None = None) -> str:
        if not file.filename:
            raise FileWithoutFilenameError

        file_extension = convert_to if convert_to else file.filename.split('.')[-1]
        if file_extension not in self.converters:
            CantConvertFile(file_extension)

        return file.filename.split('.')[0] + f".{file_extension}"

    async def _get_converted_object_with_signature(self, file: UploadFile,
                                                   system_filetype: str,
                                                   compress: bool,
                                                   convert_to: str | None = None) -> tuple[FileUrl | None, str | None]:
        await file.seek(0)
        file_bytes = await file.read()
        converter = self._get_converter_by_filename(file, convert_to)
        if not converter:
            return (None, None)

        converted_file_bytes = converter.convert(file_bytes, compress)
        converted_file_filename = self._get_new_file_filename(file, convert_to)
        converted_file = UploadFile(
            io.BytesIO(converted_file_bytes),
            filename=converted_file_filename
        )
        converted_object = await self._s3_connection.publish_object(settings.s3_bucket_name, converted_file)
        converted_object_signature = generate_signature(converted_file_filename, system_filetype)
        return (converted_object, converted_object_signature)

    def _make_saved_file_schema(self, system_filetype: str,
                                original_object: FileUrl,
                                original_signature: str,
                                converted_object: FileUrl | None = None,
                                converted_object_signature: str | None = None) -> SavedFile:
        return SavedFile(
            original_file=FileUrlWithSignature(
                system_filetype=SystemFiletypes(system_filetype),
                filename=original_object.filename,
                url=original_object.url,
                signature=original_signature
            ),
            converted_file=None if not converted_object or not converted_object_signature else FileUrlWithSignature(
                system_filetype=SystemFiletypes(system_filetype),
                filename=converted_object.filename,
                url=converted_object.url,
                signature=converted_object_signature,
            )
        )

    async def save_file(self, file: UploadFile,
                        system_filetype: str,
                        convert_to: str | None = None,
                        compress: bool = True) -> SavedFile:
        if not file.filename:
            raise FileWithoutFilenameError

        original_object = await self._s3_connection.publish_object(settings.s3_bucket_name, file)
        object_signature = generate_signature(file.filename, system_filetype)
        # TODO: Тут проверять. есть ли у пользователя пермишн на отправку не сжатых фоток
        if convert_to or compress:
            converted_object, converted_object_signature = await self._get_converted_object_with_signature(
                file, system_filetype, compress, convert_to
            )
        else:
            converted_object = None
            converted_object_signature = None

        return self._make_saved_file_schema(
            system_filetype,
            original_object,
            object_signature,
            converted_object,
            converted_object_signature,
        )


class PhotoSaver(BaseSaver):
    converters = {
        "webp": ImageWebpConverter(),
        "jpeg": ImageJpgConverter(),
        "jpg": ImageJpgConverter(),
        "png": ImagePngConverter(),
    }


class GenericSaver:

    def __init__(self, s3_connection: S3Connection):
        self._s3_connection = s3_connection

    async def save_file(self, file: UploadFile,
                        system_filetype: str) -> SavedFile:
        if not file.filename:
            raise FileWithoutFilenameError

        original_object = await self._s3_connection.publish_object(settings.s3_bucket_name, file)
        object_signature = generate_signature(file.filename, system_filetype)
        return SavedFile(original_file=FileUrlWithSignature(
            system_filetype=SystemFiletypes(system_filetype),
            filename=original_object.filename,
            url=original_object.url,
            signature=object_signature,
        ))
