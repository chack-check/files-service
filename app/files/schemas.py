from enum import Enum

from pydantic import BaseModel


class ConvertionOptions(Enum):
    webp = 'webp'


class SystemFiletypes(Enum):
    avatar = 'avatar'
    file_in_chat = 'file_in_chat'


class FileUrl(BaseModel):
    filename: str
    url: str


class FileUrlWithSignature(BaseModel):
    system_filetype: SystemFiletypes
    filename: str
    url: str
    signature: str


class GenerateAvatarRequest(BaseModel):
    metadata: str
    title: str


class SavedFile(BaseModel):
    original_file: FileUrlWithSignature
    converted_file: FileUrlWithSignature | None = None
