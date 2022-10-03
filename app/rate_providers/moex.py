"""MOEX rates scrapper."""
from decimal import Decimal

import httpx
from lxml import etree

from app import currency
from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://www.finam.ru/quote/mosbirzha-valyutnyj-rynok/{0}rubtom-{0}-rub/'
NOT_ALLOWED_CURRENCY = frozenset((currency.CZK,))


async def get_rates() -> RatesRub:
    """
    Return moex currency exchange rates.

    Raises:
        RuntimeError: For network or parsing errors.
    """
    rates = {currency_code: Decimal(0) for currency_code in NOT_ALLOWED_CURRENCY}
    moex_currency_pairs = [
        currency_code
        for currency_code in app_settings.supported_foreign_currencies
        if currency_code not in NOT_ALLOWED_CURRENCY
    ]

    async with httpx.AsyncClient() as client:
        for currency_code in moex_currency_pairs:
            try:  # noqa: WPS229
                response = await client.get(
                    url=QUOTES_ENDPOINT.format(currency_code),
                    headers={
                        b'User-Agent': app_settings.http_user_agent,
                    },
                    timeout=app_settings.http_timeout,
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise RuntimeError('network error') from fetch_exc

            try:
                rates[currency_code] = _parse_finam_rate(response.text)
            except RuntimeError as parsing_exc:
                raise RuntimeError(f'parsing error {currency_code=}') from parsing_exc

    return RatesRub(**rates)


def _parse_finam_rate(html_source: str) -> Decimal:
    try:
        html_rate = etree.HTML(html_source).xpath(
            '//span[@id="finfin-local-plugin-quote-item-review-price"]',
        )[0].get('data-quoteknownprice')

    except (AttributeError, IndexError):
        raise RuntimeError('rates not found')

    try:
        return Decimal(html_rate.replace(',', '.').strip())
    except ValueError:
        raise RuntimeError('rates corrupted')
