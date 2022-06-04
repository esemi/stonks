"""Methods for access the database."""

import aioredis

from app.rates_model import SummaryRates
from app.settings import app_settings

RATES_UPDATE_DATE_KEY = 'stonks:rates:created_at'
CASH_RATES_KEY = 'stonks:rates:cash'
FOREX_RATES_KEY = 'stonks:rates:forex'

db_pool: aioredis.Redis = aioredis.from_url(
    app_settings.redis_dsn,
    encoding='utf-8',
    decode_responses=True,
)


async def flush_rates() -> None:
    """Delete rates from database."""
    # todo test
    # todo impl
    pass


async def get_rates() -> SummaryRates:
    """Get actual rates."""
    # todo test
    # todo impl
    pass
