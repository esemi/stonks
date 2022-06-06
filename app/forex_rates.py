"""
Forex market rates scrapper from yahoo.finance API.

@see https://www.yahoofinanceapi.com/
"""

from decimal import Decimal, InvalidOperation
from json import JSONDecodeError

import httpx

from app.rates_model import RatesRub
from app.settings import app_settings

API_ENDPOINT = 'https://yfapi.net/v6/finance/quote'


async def get_forex_rates() -> RatesRub:
    """
    Return currency exchange rates from Yahoo finance.

    Raises:
        RuntimeError: For network or parsing errors.

    """
    api_request_params = {
        'region': 'US',
        'lang': 'en',
        'symbols': ','.join([
            f'{code.upper()}RUB=X'
            for code in app_settings.supported_currencies
        ]),
    }

    async with httpx.AsyncClient() as client:
        try:  # noqa: WPS229
            response = await client.get(
                url=API_ENDPOINT,
                params=api_request_params,
                headers={'X-API-KEY': app_settings.yahoo_api_token},
                timeout=app_settings.http_timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            raise RuntimeError('network error')

    try:  # noqa: WPS229
        rates = response.json(strict=False)['quoteResponse']['result']
        parsed_rates = {
            _parse_ticker(rate_source): _calculate_ticker_price(rate_source)
            for rate_source in rates
        }
        return RatesRub(**parsed_rates)
    except (JSONDecodeError, KeyError, TypeError, InvalidOperation) as exc:
        raise RuntimeError('parsing error') from exc


def _calculate_ticker_price(ticker_info: dict) -> Decimal:
    ask = Decimal(ticker_info['ask'])
    bid = Decimal(ticker_info['bid'])
    return (ask + bid) / Decimal(2)


def _parse_ticker(ticker_info: dict) -> str:
    return ticker_info['symbol'][:3].lower()
