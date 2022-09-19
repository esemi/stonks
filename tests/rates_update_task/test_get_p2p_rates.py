from decimal import Decimal

from app.rate_providers.p2p import get_rates
from app.rates_model import RatesRub


def test_get_forex_rates_czk_disabled():
    cash_rates = RatesRub(
        czk=Decimal('2.65'),
        eur=Decimal(0),
        usd=Decimal(0),
    )
    forex_rates = RatesRub(
        czk=Decimal('2.4865355'),
        eur=Decimal(0),
        usd=Decimal(0),
    )

    res = get_rates(cash_rates, forex_rates)

    assert res.czk == 0


def test_get_forex_rates_discount_applied():
    cash_rates = RatesRub(
        czk=Decimal(0),
        eur=Decimal('65.65'),
        usd=Decimal('65.64'),
    )
    forex_rates = RatesRub(
        czk=Decimal(0),
        eur=Decimal(60),
        usd=Decimal(60),
    )

    res = get_rates(cash_rates, forex_rates)

    assert res.eur == Decimal('66')
    assert res.usd == Decimal('65')


def test_get_forex_rates_forex_rate_if_greater_than():
    cash_rates = RatesRub(
        czk=Decimal(0),
        eur=Decimal('65.65'),
        usd=Decimal('65.64'),
    )
    forex_rates = RatesRub(
        czk=Decimal(0),
        eur=Decimal('65.55'),
        usd=Decimal('65.1'),
    )

    res = get_rates(cash_rates, forex_rates)

    assert res.eur == Decimal('66')
    assert res.usd == Decimal('65.1')
