from decimal import Decimal

from app import storage
from app.rates_model import RatesRub
from app.rates_update_task import _save_rates


async def test_save_rates_happy_path():
    await _save_rates(
        cash_rates=RatesRub(
            czk=Decimal('3'),
            eur=Decimal('65.1'),
            usd=Decimal('73.8'),
            cny=Decimal('12.5'),
        ),
        forex_rates=RatesRub(
            czk=Decimal('2.78'),
            eur=Decimal('60.789'),
            usd=Decimal('67.777779'),
            cny=Decimal('12.5'),
        ),
        p2p_rates=RatesRub(
            czk=Decimal('3'),
            eur=Decimal('65'),
            usd=Decimal('73'),
            cny=Decimal('12.5'),
        ),
        moex_rates=RatesRub(
            czk=Decimal('0'),
            eur=Decimal('54.0045'),
            usd=Decimal('59.0714'),
            cny=Decimal('12.5'),
        ),
    )

    assert (await storage.get_rates()) is not None
