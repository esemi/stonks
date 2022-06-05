from datetime import datetime
from decimal import Decimal

import pytest

from app.rates_model import SummaryRates, RatesRub


@pytest.fixture
async def fixture_filled_rates(mocker):
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
    mocker.patch('app.bot_app.storage.get_rates', return_value=payload)
