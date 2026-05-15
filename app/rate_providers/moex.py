"""MOEX rates scrapper."""
from decimal import Decimal
from json import JSONDecodeError

import httpx
from lxml import etree

from app import currency
from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://news.mail.ru/rate/'


async def get_rates() -> RatesRub:
    """
    Return moex currency exchange rates.

    Raises:
        RuntimeError: For network or parsing errors.
    """
    async with httpx.AsyncClient() as client:
        try:  # noqa: WPS229
            response = await client.get(
                url=QUOTES_ENDPOINT,
                headers={
                    b'User-Agent': app_settings.http_user_agent,
                },
                timeout=app_settings.http_timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as fetch_exc:
            raise RuntimeError('network error') from fetch_exc

    try:
        rates = _parse_news_mail_rate(response.text)
    except RuntimeError as parsing_exc:
        raise RuntimeError(f'parsing error {response.text=}') from parsing_exc

    return rates


def _parse_news_mail_rate(html_source: str) -> RatesRub:
    rates = {}
    html_rates = etree.HTML(html_source)

    for currency_code in app_settings.supported_foreign_currencies:
        try:  # noqa: WPS229
            currency_rate = html_rates.xpath(
                '//div/span[text()="{0}/RUB"]//ancestor::div[@class="swiper-slide"]//span[@data-qa="Title"]/text()'.format(
                    currency_code.upper(),
                ),
            )[0]
            rates[currency_code] = Decimal(currency_rate)
        except (AttributeError, IndexError, JSONDecodeError):
            raise RuntimeError('rates not found')

    rates[currency.CZK] = rates[currency.CZK] / Decimal(10)

    return RatesRub(**rates)
