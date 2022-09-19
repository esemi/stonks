"""Bloomberg exchange rates scrapper."""

from decimal import Decimal

import httpx
from lxml import etree

from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://www.bloomberg.com/quote/{0}RUB:CUR'


async def get_rates() -> RatesRub:
    """
    Return bloomberg rates.

    Raises:
        RuntimeError: For network or parsing errors.
    """
    rates = {}
    async with httpx.AsyncClient() as client:
        for currency in app_settings.supported_currencies:
            try:  # noqa: WPS229
                response = await client.get(
                    url=QUOTES_ENDPOINT.format(currency.upper()),
                    timeout=app_settings.http_timeout,
                    headers={
                        # b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        # b'Accept-Encoding': b'gzip, deflate, br',
                        b'User-Agent': app_settings.http_user_agent,
                    },
                )
                response.raise_for_status()
            except httpx.HTTPError as fetch_exc:
                raise RuntimeError('network error') from fetch_exc

            try:
                rates[currency] = _parse_bloomberg_rate(response.text)
            except RuntimeError as parsing_exc:
                raise RuntimeError('parsing error') from parsing_exc

    return RatesRub(**rates)


def _parse_bloomberg_rate(html_source: str) -> Decimal:
    try:
        html_rate = etree.HTML(html_source).cssselect(
            '.quotePageSnapshot div.pseudoMainContent section section div span',
        )[0]
    except (AttributeError, IndexError):
        raise RuntimeError('rates not found')

    return Decimal(html_rate.text)
