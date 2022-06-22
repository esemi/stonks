from app.forex_rates import get_forex_rates
from app.rates_model import RatesRub


async def test_get_forex_rates_happy_path():
    res = await get_forex_rates()

    assert isinstance(res, RatesRub)
    assert res.czk < 10
    assert res.usd
    assert res.eur
