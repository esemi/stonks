from unittest.mock import AsyncMock

from app.bot_handlers.common import log_request


async def test_save_stat_smoke(mocker):
    mock = mocker.patch('app.bot_handlers.common.storage.inc_stats')
    message_mock = AsyncMock()

    res = await log_request(message_mock)

    assert res is None
    assert mock.call_count == 1
