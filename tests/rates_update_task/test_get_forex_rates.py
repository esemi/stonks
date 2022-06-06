from decimal import Decimal

import httpx
import pytest

from app.forex_rates import get_forex_rates
from app.rates_model import RatesRub
from app.settings import app_settings


def yahoo_api_configured() -> bool:
    return len(app_settings.yahoo_api_token) > 0


async def test_get_forex_rates_happy_path(mocked_forex_rates_api):
    res = await get_forex_rates()

    assert res.czk == Decimal('1.289499999999999979571896347')
    assert res.usd == Decimal('68.5615000000000023305801733')
    assert res.eur == Decimal('83.33650000000000090949470175')


@pytest.mark.skipif(
    not yahoo_api_configured(), reason="requires configured settings.yahoo_api_token"
)
async def test_get_forex_rates_contract(mocked_forex_rates_api):
    res = await get_forex_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


async def test_get_forex_rates_network_error(mocked_rates_request):
    mocked_rates_request.mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_forex_rates()


@pytest.mark.parametrize('payload', [
    '',
    '{}',
    '{"quoteResponse": {}}',
    '{"quoteResponse": {"result": []}}',
    """{"quoteResponse": {"result": [
        {"symbol": "CZKRUB", "ask": 1.234, "bid": 1.345},
        {"symbol": "USDRUB", "ask": 67.123, "bid": 70},
        {"symbol": "EURRUB", "ask": "invalid number value", "bid": 87.123}
    ]}}""",
    """{"quoteResponse": {"result": [
        {"symbol": "CZKRUB", "ask": 1.234, "bid": 1.345},
        {"symbol": "USDRUB", "ask": 67.123, "bid": 70},
        {"symbol": "EURRUB", "ask": 81.123}
    ]}}""",
])
async def test_get_forex_rates_parsing_error(mocked_rates_request, payload: str):
    mocked_rates_request.mock(return_value=httpx.Response(200, text=payload),)

    with pytest.raises(RuntimeError, match='parsing error'):
        await get_forex_rates()
