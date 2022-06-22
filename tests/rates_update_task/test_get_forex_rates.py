import httpx
import pytest
import respx

from app.forex_rates import get_forex_rates
from app.rates_model import RatesRub


async def test_get_forex_rates_happy_path():
    res = await get_forex_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


@respx.mock(base_url="https://www.xe.com/currencyconverter/convert/", assert_all_mocked=False)
async def test_get_cash_rates_network_error(respx_mock):
    respx_mock.get("?Amount=1&From=CZK&To=RUB").mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_forex_rates()
