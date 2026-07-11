from unittest.mock import AsyncMock

from app.bot_handlers.details import rate_details_handler
from app.bot_handlers.stonks import current_rates_handler
from app.bot_handlers.welcome import welcome_handler


def _build_message_mock(text: str) -> AsyncMock:
    message_mock = AsyncMock()
    message_mock.text = text
    message_mock.chat.username = None
    message_mock.chat.title = None
    return message_mock


async def test_welcome_handler():
    message_mock = _build_message_mock('/help')

    await welcome_handler(message=message_mock)

    message_mock.reply.assert_called_once()


async def test_current_rates_handler(fixture_filled_rates):
    message_mock = _build_message_mock('/stonks')

    await current_rates_handler(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_details_handler(fixture_filled_rates):
    message_mock = _build_message_mock('/details')

    await rate_details_handler(message=message_mock)

    message_mock.answer.assert_called_once()
