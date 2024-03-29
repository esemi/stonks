"""Methods for access the database."""
from dataclasses import asdict
from datetime import datetime

import aioredis

from app.rates_model import RatesRub, SummaryRates
from app.settings import app_settings

RATES_UPDATE_DATE_KEY = 'stonks:rates:created_at'
CASH_RATES_KEY = 'stonks:rates:cash'
FOREX_RATES_KEY = 'stonks:rates:forex'
P2P_RATES_KEY = 'stonks:rates:p2p'
MOEX_RATES_KEY = 'stonks:rates:moex'
BOT_STATS_COMMAND_KEY = 'stonks:stats:command:{0}'
BOT_STATS_CHAT_KEY = 'stonks:stats:chat:{0}'

db_pool: aioredis.Redis = aioredis.from_url(
    app_settings.redis_dsn,
    encoding='utf-8',
    decode_responses=True,
)


async def get_rates() -> SummaryRates:
    """Get actual rates."""
    cash_rates = await db_pool.hgetall(CASH_RATES_KEY)
    forex_rates = await db_pool.hgetall(FOREX_RATES_KEY)
    p2p_rates = await db_pool.hgetall(P2P_RATES_KEY)
    moex_rates = await db_pool.hgetall(MOEX_RATES_KEY)
    created_at = await db_pool.get(RATES_UPDATE_DATE_KEY)
    return SummaryRates(
        created_at=datetime.fromisoformat(created_at),
        cash=RatesRub.from_dict(cash_rates),
        forex=RatesRub.from_dict(forex_rates),
        p2p=RatesRub.from_dict(p2p_rates),
        moex=RatesRub.from_dict(moex_rates),
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
    await db_pool.hset(P2P_RATES_KEY, mapping={
        currency: str(rate)
        for currency, rate in asdict(rates.p2p).items()
    })
    await db_pool.hset(MOEX_RATES_KEY, mapping={
        currency: str(rate)
        for currency, rate in asdict(rates.moex).items()
    })
    await db_pool.set(RATES_UPDATE_DATE_KEY, str(datetime.utcnow()))


async def inc_stats(method: str, chat_id: int) -> None:
    """Save call counter."""
    await db_pool.incr(BOT_STATS_COMMAND_KEY.format(method))
    await db_pool.incr(BOT_STATS_CHAT_KEY.format(chat_id))
