from enum import Enum

import strawberry


@strawberry.enum
class SystemFiletypesEnum(Enum):
    avatar = "avatar"
    file_in_chat = "file_in_chat"
    voice = "voice"
    circle = "circle"


@strawberry.enum
class ConvertionOptionsEnum(Enum):
    webp = "webp"


@strawberry.type
class UploadedFileMeta:
    system_filetype: SystemFiletypesEnum
    filename: str
    url: str
    signature: str


@strawberry.type
class UploadedFile:
    original_file: UploadedFileMeta
    converted_file: UploadedFileMeta | None
