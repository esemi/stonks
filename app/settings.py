"""Application settings."""
import os
from decimal import Decimal
from typing import List

from pydantic import BaseSettings, Field, RedisDsn


class AppSettings(BaseSettings):
    """Application settings class."""

    redis_dsn: RedisDsn = Field('redis://localhost:6379/2')
    http_timeout: int = Field(35, description='rates-API request timeout')
    http_user_agent: bytes = Field(
        default=b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/74.0.3729.169 Safari/537.36',
    )
    throttling_time: float = Field(60.0 * 10, description='Seconds between update rate tries in seconds')
    throttling_min_time: float = 10.0
    p2p_rate_discount: Decimal = Field(Decimal('0.15'), description='P2P rate discount from cash rates in ruble cents')
    debug: bool = Field(default=False)
    telegram_token: str
    supported_currencies: List[str] = ['czk', 'eur', 'usd']


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
