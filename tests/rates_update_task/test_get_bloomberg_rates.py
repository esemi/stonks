import pytest
import requests

from app.rate_providers.bloomberg import get_rates
from app.rates_model import RatesRub


async def test_get_bloomberg_rates_contract():
    res = await get_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd > 1
    assert res.eur > 1


async def test_get_bloomberg_rates_network_error(mocker):
    mocker.patch('activesoup.Driver.get', side_effect=requests.RequestException(502))

    with pytest.raises(RuntimeError, match='network error'):
        await get_rates()
