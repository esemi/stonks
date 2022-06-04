"""Application settings."""
import os

from pydantic import BaseSettings, Field, RedisDsn


class AppSettings(BaseSettings):
    """Application settings class."""

    redis_dsn: RedisDsn = Field('redis://localhost:6379/2')
    http_timeout: int = Field(35, description='rates-API request timeout')
    throttling_time: float = Field(600.0, description='Seconds between update rate tries')
    debug: bool = Field(default=False)


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
