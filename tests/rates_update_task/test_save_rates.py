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
        ),
        forex_rates=RatesRub(
            czk=Decimal('2.78'),
            eur=Decimal('60.789'),
            usd=Decimal('67.777779'),
        ),
        p2p_rates=RatesRub(
            czk=Decimal('3'),
            eur=Decimal('65'),
            usd=Decimal('73'),
        ),
        bloomberg_rates=RatesRub(
            czk=Decimal('2.78'),
            eur=Decimal('60.789'),
            usd=Decimal('67.777779'),
        ),
    )

    assert (await storage.get_rates()) is not None
