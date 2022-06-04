import pytest

from app.rates_model import RatesRub
from app.rates_update_task import _get_cash_rates
import respx
import httpx


async def test_get_cash_rates_happy_path():
    res = await _get_cash_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur


@respx.mock(base_url="https://blagodatka.ru/detailed", assert_all_mocked=False)
async def test_get_cash_rates_network_error(respx_mock):
    respx_mock.get("/eur").mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await _get_cash_rates()
