"""Methods for access the database."""
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

import aioredis

from app.rates_model import RatesRub, SummaryRates
from app.settings import app_settings

RATES_UPDATE_DATE_KEY = 'stonks:rates:created_at'
CASH_RATES_KEY = 'stonks:rates:cash'
FOREX_RATES_KEY = 'stonks:rates:forex'

db_pool: aioredis.Redis = aioredis.from_url(
    app_settings.redis_dsn,
    encoding='utf-8',
    decode_responses=True,
)


async def get_rates() -> SummaryRates:
    """Get actual rates."""
    cash_rates = await db_pool.hgetall(CASH_RATES_KEY)
    forex_rates = await db_pool.hgetall(FOREX_RATES_KEY)
    created_at = await db_pool.get(RATES_UPDATE_DATE_KEY)
    return SummaryRates(
        created_at=created_at,
        cash=RatesRub(**{
            currency: Decimal(rate)
            for currency, rate in cash_rates.items()
        }),
        forex=RatesRub(**{
            currency: Decimal(rate)
            for currency, rate in forex_rates.items()
        }),
    )


async def save_rates(rates: SummaryRates) -> None:
    """Update actual rates."""
    await db_pool.hset(CASH_RATES_KEY, mapping={
        currency: str(rate)
        for currency, rate in asdict(rates.cash).items()
    })
    await db_pool.hset(FOREX_RATES_KEY, mapping={
        currency: str(rate)
        for currency, rate in asdict(rates.forex).items()
    })
    await db_pool.set(RATES_UPDATE_DATE_KEY, str(datetime.utcnow()))
