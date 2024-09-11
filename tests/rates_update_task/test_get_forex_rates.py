from app.rate_providers.forex import get_rates
from app.rates_model import RatesRub


async def test_get_forex_rates_happy_path():
    res = await get_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur
    assert res.cny
