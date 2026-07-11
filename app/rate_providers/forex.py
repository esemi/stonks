"""Forex rates scrapper."""
from decimal import Decimal
from json import JSONDecodeError

import httpx

from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://markets.ft.com/data/currencies/ajax/conversion'


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
                        'amount': 1,
                        'baseCurrency': currency.upper(),
                        'comparison': 'RUB',
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
                rates[currency] = _parse_rate(response.json())
            except (RuntimeError, JSONDecodeError) as parsing_exc:
                raise RuntimeError('parsing error') from parsing_exc

    return RatesRub(**rates)


def _parse_rate(json_response: dict) -> Decimal:
    try:
        rate = json_response['data']['exchangeRate']
    except (AttributeError, IndexError) as err:
        raise RuntimeError('rates not found') from err

    try:
        return Decimal(rate)
    except ValueError as err:
        raise RuntimeError('rates corrupted') from err
