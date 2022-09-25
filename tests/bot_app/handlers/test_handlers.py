from unittest.mock import AsyncMock
from app.bot_handlers.details import rate_details_handler
from app.bot_handlers.stonks import current_rates_handler
from app.bot_handlers.welcome import welcome_handler


async def test_welcome_handler():
    message_mock = AsyncMock()

    await welcome_handler(message=message_mock)

    message_mock.reply.assert_called_once()


async def test_current_rates_handler(fixture_filled_rates):
    message_mock = AsyncMock()

    await current_rates_handler(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_details_handler(fixture_filled_rates):
    message_mock = AsyncMock()

    await rate_details_handler(message=message_mock)

    message_mock.answer.assert_called_once()
