import asyncio

import pytest

from app.storage import flush_rates


@pytest.fixture()
async def fixture_empty_database():
    await flush_rates()
    yield


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
