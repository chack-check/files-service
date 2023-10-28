from ..settings import settings

from .s3 import S3Connection


def use_s3_connection() -> S3Connection:
    conn = S3Connection(settings.s3_endpoint_url)
    return conn
