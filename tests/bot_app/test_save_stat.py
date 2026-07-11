from unittest.mock import AsyncMock

from app.bot_handlers.common import log_request


async def test_save_stat_smoke():
    message_mock = AsyncMock()
    message_mock.text = '/stonks'
    message_mock.chat.username = None
    message_mock.chat.title = None

    res = await log_request(message_mock)

    assert res is None
