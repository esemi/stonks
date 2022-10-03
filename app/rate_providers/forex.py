"""Forex rates scrapper."""
import uuid
from decimal import Decimal

import httpx
from lxml import etree

from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://www.xe.com/currencyconverter/convert/'


async def get_rates() -> RatesRub:
    """
    Return forex currency exchange rates.

    Raises:
        RuntimeError: For network or parsing errors.
    """
    rates = {}
    async with httpx.AsyncClient() as client:
        for currency in app_settings.supported_foreign_currencies:
            try:  # noqa: WPS229
                response = await client.get(
                    QUOTES_ENDPOINT,
                    params={
                        'Amount': 1,
                        'From': currency.upper(),
                        'To': 'RUB',
                        'random_hash': uuid.uuid4().hex,
                    },
                    headers={
                        b'User-Agent': app_settings.http_user_agent,
                    },
                    timeout=app_settings.http_timeout,
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise RuntimeError('network error') from fetch_exc

            try:
                rates[currency] = _parse_xe_rate(response.text)
            except RuntimeError as parsing_exc:
                raise RuntimeError('parsing error') from parsing_exc

    return RatesRub(**rates)


def _parse_xe_rate(html_source: str) -> Decimal:
    stringify = etree.XPath('string()')
    try:
        html_rate = stringify(etree.HTML(html_source).xpath('//main/form//p')[1])

    except (AttributeError, IndexError):
        raise RuntimeError('rates not found')

    try:
        return Decimal(html_rate.replace('Russian Rubles', '').strip())
    except ValueError:
        raise RuntimeError('rates corrupted')
