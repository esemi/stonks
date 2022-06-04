from unittest.mock import AsyncMock
from app.bot_app import welcome_handler, current_rates_handler


async def test_welcome_handler():
    message_mock = AsyncMock()

    await welcome_handler(message=message_mock)

    message_mock.reply.assert_called_once()


async def test_current_rates_handler():
    message_mock = AsyncMock()

    await current_rates_handler(message=message_mock)

    message_mock.answer.assert_called_once()
