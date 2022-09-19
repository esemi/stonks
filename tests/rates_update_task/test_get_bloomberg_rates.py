import httpx
import pytest
import respx

from app.rates_model import RatesRub
from app.bloomberg_rates import get_bloomberg_rates


async def test_get_bloomberg_rates_contract():
    res = await get_bloomberg_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


@respx.mock(assert_all_mocked=False)
async def test_get_bloomberg_rates_network_error(respx_mock):
    respx_mock.get("https://www.bloomberg.com/quote/CZKRUB:CUR").mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_bloomberg_rates()
