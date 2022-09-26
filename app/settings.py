"""Application settings."""
import os
from decimal import Decimal
from typing import List

from pydantic import BaseSettings, Field, RedisDsn

from app import currency


class AppSettings(BaseSettings):
    """Application settings class."""

    redis_dsn: RedisDsn = Field('redis://localhost:6379/3')
    http_timeout: int = Field(45, description='rates-API request timeout')
    http_user_agent: bytes = Field(
        default=b'Mozilla/5.0 (X11; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/536.36"',
    )
    throttling_time: float = Field(60.0 * 20, description='Seconds between update rate tries in seconds')
    throttling_min_time: float = 10.0
    p2p_rate_discount: Decimal = Field(Decimal('0.15'), description='P2P rate discount from cash rates in ruble cents')
    debug: bool = Field(default=False)
    telegram_token: str
    supported_foreign_currencies: List[str] = [currency.CZK, currency.EUR, currency.USD]
    currency_aliases: dict[str, str] = {
        'czk': currency.CZK,
        'крон': currency.CZK,
        'kč': currency.CZK,

        'usd': currency.USD,
        'баксов': currency.USD,
        'бакса': currency.USD,
        'бакс': currency.USD,
        '$': currency.USD,

        'eur': currency.EUR,
        'евро': currency.EUR,
        'евров': currency.EUR,
        '€': currency.EUR,

        'rub': currency.RUB,
        'rur': currency.RUB,
        'рублей': currency.RUB,
        'рубля': currency.RUB,
        'руб': currency.RUB,
        'р': currency.RUB,
    }


app_settings = AppSettings(
    _env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
)
