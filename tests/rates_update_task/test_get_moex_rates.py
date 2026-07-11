import httpx
import pytest
import respx

from app.rate_providers.moex import QUOTES_ENDPOINT, get_rates
from app.rates_model import RatesRub


async def test_get_moex_rates_contract():
    res = await get_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd > 10
    assert res.eur > 10
    assert res.cny > 10


@respx.mock(base_url=QUOTES_ENDPOINT, assert_all_mocked=False)
async def test_get_moex_rates_network_error(respx_mock):
    respx_mock.get('').mock(return_value=httpx.Response(403))

    with pytest.raises(RuntimeError, match='network error'):
        await get_rates()


@respx.mock(base_url=QUOTES_ENDPOINT, assert_all_mocked=False)
async def test_get_moex_rates_invalid_content(respx_mock):
    respx_mock.get('').mock(return_value=httpx.Response(200, content='sdsd sd sd sds'))

    with pytest.raises(RuntimeError, match='parsing error'):
        await get_rates()
