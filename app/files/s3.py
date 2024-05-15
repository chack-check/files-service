from uuid import uuid4

import boto3
from fastapi import UploadFile

from .exceptions import IncorrectFileName
from .schemas import FileUrl


class S3Connection:

    def __init__(self, endpoint_url: str) -> None:
        self._endpoint_url = endpoint_url
        self._session = boto3.Session()
        self._client = self._session.client(
            service_name="s3",
            endpoint_url=endpoint_url,
        )

    def _generate_file_key_for_filename(self, filename: str) -> str:
        file_uuid = str(uuid4())
        file_extension = filename.split(".")[-1]
        key = f"{file_uuid}.{file_extension}"
        return key

    def _get_url_for_key(self, bucket_name: str, key: str) -> str:
        return f"{self._endpoint_url}/{bucket_name}/{key}"

    def _validate_filename(self, filename: str | None) -> None:
        if not filename:
            raise IncorrectFileName()

    async def _put_object(self, bucket_name: str, key: str, file: UploadFile) -> None:
        file_body = await file.read()
        self._client.put_object(Bucket=bucket_name, Key=key, Body=file_body)

    async def publish_object(self, bucket_name: str, file: UploadFile) -> FileUrl:
        self._validate_filename(file.filename)
        assert file.filename
        key = self._generate_file_key_for_filename(file.filename)
        url = self._get_url_for_key(bucket_name, key)
        await self._put_object(bucket_name, key, file)
        return FileUrl(filename=file.filename, url=url)
