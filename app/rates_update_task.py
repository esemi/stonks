"""This module periodically update actual cash and forex rates to the database."""

import asyncio
import logging
from collections import Counter
from typing import Optional

from app.rates_model import RatesRub
from app.settings import app_settings

# todo catch signint


async def main(throttling_time: float, max_iterations: Optional[int] = None) -> Counter:
    """
    Background task for update rates.

    Update currency rates
        - from ligovka.ru - for actual cash exchange rates from Russia
        - from forex - for actual exchange rate from abroad Russia

    Support USD.RUB, CZK.RUB and EUR.RUB
    """
    cnt = Counter(
        iteration=0,
        fails=0,
        success=0,
    )
    while not max_iterations or cnt['iteration'] < max_iterations:
        cnt['iteration'] += 1
        if cnt['iteration'] > 1:
            await asyncio.sleep(throttling_time)

        logging.info(f'Current iteration is {cnt}')

        try:
            cash_rates, forex_rates = await asyncio.gather(
                _get_cash_rates(),
                _get_forex_rates(),
            )
        except RuntimeError as exc:
            cnt['fails'] += 1
            logging.warning(f'exception in getting rates process {exc}')
            continue

        logging.info(f'Get rates: {cash_rates=}, {forex_rates=}')

        await _save_rates(cash_rates, forex_rates)
        cnt['success'] += 1

    return cnt


async def _save_rates(cash_rates: RatesRub, forex_rates: RatesRub) -> bool:
    # todo impl
    # todo test
    pass


async def _get_cash_rates() -> RatesRub:
    # todo impl
    # todo test
    pass


async def _get_forex_rates() -> RatesRub:
    # todo impl
    # todo test
    pass


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    asyncio.run(main(
        throttling_time=app_settings.throttling_time,
        max_iterations=None,
    ))
