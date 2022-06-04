from datetime import datetime
from decimal import Decimal

from app.rates_model import SummaryRates, RatesRub
from app.storage import save_rates, get_rates


async def test_save_rates_happy_path():
    payload = SummaryRates(
        created_at=datetime.utcnow(),
        cash=RatesRub(
            czk=Decimal('3'),
            eur=Decimal('65.1'),
            usd=Decimal('73.8'),
        ),
        forex=RatesRub(
            czk=Decimal('2.78'),
            eur=Decimal('60.789'),
            usd=Decimal('67.777779'),
        ),
    )

    res = await save_rates(payload)

    saved_rates = await get_rates()
    assert res is None
    assert saved_rates.created_at
    assert saved_rates.cash.eur == Decimal('65.1')
    assert saved_rates.forex.usd == Decimal('67.777779')
