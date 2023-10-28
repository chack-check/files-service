from pydantic import BaseModel


class FileUrl(BaseModel):
    filename: str
    url: str


class GenerateAvatarRequest(BaseModel):
    metadata: str
    title: str
