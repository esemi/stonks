from app.storage import inc_stats


async def test_inc_stats_smoke():
    res = await inc_stats('test method', 123)

    assert res is None
