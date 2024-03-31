from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env'
    )

    s3_endpoint_url: str
    signature_key: str
    secret_key: str
    compression_size: int = 70
    run_mode: str = 'dev'
    s3_bucket_name: str = 'chackcheck'
    max_avatar_video_duration: int = 10
    allowed_origins: list[str] = ['*']
    sentry_dsn: str | None = None


settings = Settings()
