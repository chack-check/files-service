from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env'
    )

    run_mode: str = 'dev'
    s3_endpoint_url: str
    s3_bucket_name: str = 'chackcheck'
    secret_key: str
    allowed_origins: list[str] = ['*']


settings = Settings()
