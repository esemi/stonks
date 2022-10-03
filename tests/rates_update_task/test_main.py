from app import storage
from app.rates_model import SummaryRates
from app.rates_update_task import main


async def test_main_happy_path(fixture_filled_rates: SummaryRates, mocker):
    mocker.patch('app.rates_update_task.forex.get_rates', return_value=fixture_filled_rates.forex)
    mocker.patch('app.rates_update_task.cash.get_rates', return_value=fixture_filled_rates.cash)
    mocker.patch('app.rates_update_task.p2p.get_rates', return_value=fixture_filled_rates.p2p)
    mocker.patch('app.rates_update_task.moex.get_rates', return_value=fixture_filled_rates.moex)

    res = await main(throttling_max_time=1.0, max_iterations=2)

    assert res['success'] == 2
    assert res['iteration'] == 2
    assert res['fails'] == 0
    assert (await storage.get_rates()) is not None
