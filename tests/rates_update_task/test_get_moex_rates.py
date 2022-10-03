import httpx
import pytest
import respx

from app.rates_model import RatesRub
from app.rate_providers.moex import get_rates


async def test_get_moex_rates_contract():
    res = await get_rates()

    assert isinstance(res, RatesRub)
    assert res.czk == 0
    assert res.usd > 10
    assert res.eur > 10


@respx.mock(base_url="https://www.finam.ru/quote/mosbirzha-valyutnyj-rynok", assert_all_mocked=False)
async def test_get_moex_rates_network_error(respx_mock):
    respx_mock.get('/eurrubtom-eur-rub/').mock(return_value=httpx.Response(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_rates()
