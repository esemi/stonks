"""Bloomberg exchange rates scrapper."""

from decimal import Decimal

import activesoup
from lxml import etree
from requests import RequestException

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
    browser_driver = activesoup.Driver(
        headers={'User-Agent': app_settings.http_user_agent},
        timeout=app_settings.http_timeout,
    )
    for currency in app_settings.supported_currencies:
        url = QUOTES_ENDPOINT.format(currency.upper())
        try:
            response = browser_driver.get(url).last_response
        except RequestException as fetch_exc:
            raise RuntimeError('network error') from fetch_exc

        try:
            rates[currency] = _parse_bloomberg_rate(response.html())
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
