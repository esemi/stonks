"""This module periodically update actual cash and forex rates to the database."""

import asyncio
import logging
import signal
from collections import Counter
from datetime import datetime
from typing import Optional

from app import storage
from app.cash_rates import get_cash_rates
from app.forex_rates import get_forex_rates
from app.p2p_rates import get_p2p_rates
from app.rates_model import RatesRub, SummaryRates
from app.settings import app_settings

FORCE_SHUTDOWN = False


def sigint_handler(current_signal, frame) -> None:  # type: ignore
    """Handle correct signal for restart service."""
    global FORCE_SHUTDOWN  # noqa: WPS420
    FORCE_SHUTDOWN = True  # noqa: WPS442


async def main(throttling_max_time: float, max_iterations: Optional[int] = None) -> Counter:  # noqa: WPS231
    """
    Background task for update rates.

    Update currency rates
        - from ligovka.ru - for actual cash exchange rates from Russia
        - from forex - for actual exchange rate from abroad Russia
          and calculate actual p2p rate by cash-rates

    Support USD.RUB, CZK.RUB and EUR.RUB
    """
    cnt: Counter = Counter(
        iteration=0,
        fails=0,
        success=0,
    )
    throttling_timer: float = 0
    throttling_timer_chunk: float = min(app_settings.throttling_min_time, throttling_max_time)
    while not max_iterations or cnt['iteration'] < max_iterations:
        if FORCE_SHUTDOWN:
            break

        if cnt['iteration']:
            if throttling_timer < throttling_max_time:
                logging.debug(f'sleep chunk time {throttling_timer=} {throttling_max_time}')
                throttling_timer += throttling_timer_chunk
                await asyncio.sleep(throttling_timer_chunk)
                continue
            else:
                logging.debug('sleep time end')
                throttling_timer = 0

        cnt['iteration'] += 1
        logging.info(f'Current iteration {cnt=}')

        ok = await _update_rate()
        cnt['success' if ok else 'fails'] += 1

    logging.info(f'shutdown {cnt=}')
    return cnt


async def _update_rate() -> bool:
    try:
        cash_rates, forex_rates = await asyncio.gather(
            get_cash_rates(),
            get_forex_rates(),
        )
    except RuntimeError as exc:
        logging.warning(f'exception in getting rates process {exc}', exc_info=exc)
        return False

    p2p_rates = get_p2p_rates(cash_rates, forex_rates)

    logging.info(f'Get rates: {cash_rates=}, {forex_rates=}, {p2p_rates=}')

    await _save_rates(cash_rates, forex_rates, p2p_rates)
    return True


async def _save_rates(cash_rates: RatesRub, forex_rates: RatesRub, p2p_rates: RatesRub) -> None:
    summary_rates = SummaryRates(
        created_at=datetime.utcnow(),
        cash=cash_rates,
        forex=forex_rates,
        p2p=p2p_rates,
    )
    await storage.save_rates(summary_rates)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    signal.signal(signal.SIGINT, sigint_handler)

    asyncio.run(main(
        throttling_max_time=app_settings.throttling_time,
        max_iterations=None,
    ))
