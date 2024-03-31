from app.files.schemas import FileUrlWithSignature, SavedFile
from app.graph.types import SystemFiletypesEnum, UploadedFile, UploadedFileMeta


class FileFactory:
    @classmethod
    def file_meta_to_schema(cls, file_meta: FileUrlWithSignature) -> UploadedFileMeta:
        return UploadedFileMeta(
            system_filetype=SystemFiletypesEnum(file_meta.system_filetype.value),
            filename=file_meta.filename,
            url=file_meta.url,
            signature=file_meta.signature,
        )

    @classmethod
    def saved_file_to_schema(cls, file: SavedFile) -> UploadedFile:
        return UploadedFile(
            original_file=cls.file_meta_to_schema(file.original_file),
            converted_file=cls.file_meta_to_schema(file.converted_file) if file.converted_file else None,
        )
