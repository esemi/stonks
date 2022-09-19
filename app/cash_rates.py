"""Cash exchange point rates scrapper."""

from decimal import Decimal

import httpx
from lxml import etree

from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://blagodatka.ru/detailed/{0}'


async def get_cash_rates() -> RatesRub:
    """
    Return cash currency exchange rates.

    Raises:
        RuntimeError: For network or parsing errors.
    """
    currency_factor = {
        # code: exchange factor
        'czk': 10,
    }
    rates = {}
    async with httpx.AsyncClient() as client:
        for currency in app_settings.supported_currencies:
            try:  # noqa: WPS229
                response = await client.get(
                    QUOTES_ENDPOINT.format(currency),
                    timeout=app_settings.http_timeout,
                    headers={
                        b'User-Agent': app_settings.http_user_agent,
                    },
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise RuntimeError('network error') from fetch_exc

            try:
                rate = _parse_ligovka_rate(response.text)
            except RuntimeError as parsing_exc:
                raise RuntimeError('parsing error') from parsing_exc

            rates[currency] = rate / Decimal(currency_factor.get(currency, 1))

    return RatesRub(**rates)


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
