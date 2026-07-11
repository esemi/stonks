from app.bot_app import main


async def test_main_smoke(mocker):
    mock = mocker.patch('app.bot_app.dp.start_polling')

    res = await main()

    assert res is None
    assert mock.call_count == 1
