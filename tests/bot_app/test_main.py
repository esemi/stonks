from app.bot_app import main


def test_main_smoke(mocker):
    mock = mocker.patch('app.bot_app.executor.start_polling')

    res = main()

    assert res is None
    assert mock.call_count == 1
