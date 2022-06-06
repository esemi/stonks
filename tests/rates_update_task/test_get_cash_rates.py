import httpx
import pytest
import respx

from app.rates_model import RatesRub
from app.cash_rates import get_cash_rates


async def test_get_cash_rates_contract():
    res = await get_cash_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


@respx.mock(base_url="https://blagodatka.ru/detailed", assert_all_mocked=False)
async def test_get_cash_rates_network_error(respx_mock):
    respx_mock.get("/czk").mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_cash_rates()
