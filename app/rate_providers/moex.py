"""MOEX rates scrapper."""
from decimal import Decimal
from json import JSONDecodeError

import httpx

from app.rates_model import RatesRub
from app.settings import app_settings

QUOTES_ENDPOINT = 'https://news.mail.ru/rate/ext/rate_initial/RUB/'


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
        rates = _parse_news_mail_rate(response)
    except RuntimeError as parsing_exc:
        raise RuntimeError(f'parsing error {response.text=}') from parsing_exc

    return rates


def _parse_news_mail_rate(response: httpx.Response) -> RatesRub:
    rates = {}

    try:  # noqa: WPS229
        for source_rate in response.json()['data']['currency_rates']['CBRF']['rows']:
            currency_code = source_rate['code'].lower()
            if currency_code in app_settings.supported_foreign_currencies:
                rates[currency_code] = Decimal(
                    source_rate['rate']['value'] / source_rate['rate']['nominal'],
                )

    except (AttributeError, IndexError, JSONDecodeError):
        raise RuntimeError('rates not found')

    return RatesRub(**rates)
