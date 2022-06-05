import httpx
import pytest
import respx

from app.rates_model import RatesRub
from app.forex_rates import get_forex_rates


async def test_get_forex_rates_happy_path():
    res = await get_forex_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


@respx.mock(base_url="https://api.exchangerate.host", assert_all_mocked=False)
async def test_get_forex_rates_network_error(respx_mock):
    respx_mock.get("/latest?base=RUB").mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_forex_rates()


@pytest.mark.parametrize('payload', [
    '',
    """{"rates":{"USD":0.05799,"EUR":1.404665}}""",
])
async def test_get_forex_rates_parsing_error(respx_mock, payload: str):
    respx_mock.get("https://api.exchangerate.host/latest?base=RUB").mock(return_value=httpx.Response(200, text=payload))

    with pytest.raises(RuntimeError, match='parsing error'):
        await get_forex_rates()
