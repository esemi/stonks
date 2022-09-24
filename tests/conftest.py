import asyncio
from datetime import datetime
from decimal import Decimal

import pytest

from app.rates_model import SummaryRates, RatesRub


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def fixture_filled_rates(mocker) -> SummaryRates:
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
        p2p=RatesRub(
            czk=Decimal('3'),
            eur=Decimal('64'),
            usd=Decimal('73'),
        ),
        bloomberg=RatesRub(
            czk=Decimal('2.78'),
            eur=Decimal('60.789'),
            usd=Decimal('67.777779'),
        ),
    )
    mocker.patch('app.storage.get_rates', return_value=payload)
    yield payload
