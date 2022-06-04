"""This module periodically update actual cash and forex rates to the database."""

import asyncio
import logging
from collections import Counter
from datetime import datetime
from decimal import Decimal
from json import JSONDecodeError
from typing import Optional

import httpx
from lxml import etree

from app import storage
from app.rates_model import RatesRub, SummaryRates
from app.settings import app_settings


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

        logging.info(f'Current iteration {cnt=}')

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


async def _save_rates(cash_rates: RatesRub, forex_rates: RatesRub) -> None:
    # todo test
    summary_rates = SummaryRates(
        created_at=datetime.utcnow(),
        cash=cash_rates,
        forex=forex_rates,
    )
    await storage.save_rates(summary_rates)


async def _get_cash_rates() -> RatesRub:
    supported_currencies = {
        # code: exchange factor
        'eur': 1,
        'czk': 10,
        'usd': 1,
    }
    rates = {}
    async with httpx.AsyncClient() as client:
        for currency, factor in supported_currencies.items():
            try:  # noqa: WPS229
                response = await client.get(
                    f'https://blagodatka.ru/detailed/{currency}',
                    timeout=app_settings.http_timeout,
                )
                response.raise_for_status()
            except httpx.HTTPError:
                raise RuntimeError('network error')

            try:
                rate = _parse_ligovka_rate(response.text)
            except RuntimeError as exc:
                raise RuntimeError('parsing error') from exc

            rates[currency] = rate / Decimal(factor)

    return RatesRub(**rates)


async def _get_forex_rates() -> RatesRub:
    async with httpx.AsyncClient() as client:
        try:  # noqa: WPS229
            response = await client.get(
                'https://api.exchangerate.host/latest?base=RUB',
                timeout=app_settings.http_timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            raise RuntimeError('network error')

    try:  # noqa: WPS229
        rates = response.json(strict=False)['rates']
        return RatesRub(
            czk=Decimal(1) / Decimal(rates.get('CZK')),
            eur=Decimal(1) / Decimal(rates.get('EUR')),
            usd=Decimal(1) / Decimal(rates.get('USD')),
        )
    except (JSONDecodeError, TypeError) as exc:
        raise RuntimeError('parsing error') from exc


def _parse_ligovka_rate(html_source: str) -> Decimal:
    try:
        html_rate = etree.HTML(html_source).cssselect('.table_course tr')[2]
    except (AttributeError, IndexError):
        raise RuntimeError('rates not found')

    try:
        buy_rate, sell_rate = html_rate.cssselect('.money_price')
    except ValueError:
        raise RuntimeError('rates corrupted')

    return (Decimal(sell_rate.text) + Decimal(buy_rate.text)) / Decimal(2)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    asyncio.run(main(
        throttling_time=app_settings.throttling_time,
        max_iterations=None,
    ))
