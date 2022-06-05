"""Forex market rates scrapper."""

from decimal import Decimal
from json import JSONDecodeError

import httpx

from app.rates_model import RatesRub
from app.settings import app_settings


async def get_forex_rates() -> RatesRub:
    """
    Return currency exchange rates from Forex market.

    Raises:
        RuntimeError: For network or parsing errors.
    """
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
        parsed_rates = {
            code: Decimal(1) / Decimal(rates.get(code.upper()))
            for code in app_settings.supported_currencies
        }
    except (JSONDecodeError, TypeError) as exc:
        raise RuntimeError('parsing error') from exc

    return RatesRub(**parsed_rates)
