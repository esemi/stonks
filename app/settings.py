"""Application settings."""
import os
from typing import List

from pydantic import BaseSettings, Field, RedisDsn


class AppSettings(BaseSettings):
    """Application settings class."""

    redis_dsn: RedisDsn = Field('redis://localhost:6379/2')
    http_timeout: int = Field(35, description='rates-API request timeout')
    throttling_time: float = Field(60.0 * 20, description='Seconds between update rate tries')
    throttling_min_time: float = 10.0
    debug: bool = Field(default=False)
    telegram_token: str
    yahoo_api_token: str
    supported_currencies: List[str] = ['czk', 'eur', 'usd']


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
