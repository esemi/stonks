from unittest.mock import AsyncMock

from app.bot_app import _save_stat


async def test_save_stat_smoke(mocker):
    mock = mocker.patch('app.bot_app.storage.inc_stats')
    message_mock = AsyncMock()

    res = await _save_stat(message_mock)

    assert res is None
    assert mock.call_count == 1
