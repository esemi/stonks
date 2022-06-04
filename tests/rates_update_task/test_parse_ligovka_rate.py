from decimal import Decimal

import pytest

from app.rates_update_task import _parse_ligovka_rate


async def test_parse_ligovka_rate_happy_path():
    valid_html = """
    <div class="col-course">
        <table class="table_course">
            <tbody>
            <tr class="actions_with_money">
                <td colspan="2"></td>
                <td class="buy_col">Покупка</td>
                <td class="sale_col">Продажа</td>
            </tr>
                                <tr>
                    <td class="money_quantity">от 1</td>
                    <td class="money_icon"><img src="/images/icons/ic-money1.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">73.045</td>
                    <td class="money_price">71.50</td>
                </tr>
                                <tr>
                    <td class="money_quantity">от 1000</td>
                    <td class="money_icon"><img src="/images/icons/ic-money1000.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">75.58</td>
                    <td class="money_price">78.55</td>
                </tr>
                                <tr>
                    <td class="money_quantity">от 10000</td>
                    <td class="money_icon"><img src="/images/icons/ic-money10000.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">77.456</td>
                    <td class="money_price">79.50</td>
                </tr>
                            </tbody></table>
    </div>
    """

    res = _parse_ligovka_rate(valid_html)

    assert res == (Decimal('78.55') + Decimal('75.58')) / Decimal(2)


async def test_parse_ligovka_rate_czk():
    valid_czk_html = """<table class="table_course">
                <tbody>
                <tr class="actions_with_money">
                    <td colspan="2"></td>
                    <td class="buy_col">Покупка</td>
                    <td class="sale_col">Продажа</td>
                </tr>
                                    <tr>
                        <td class="money_quantity">от 1</td>
                        <td class="money_icon"><img src="/images/icons/ic-money1.png" alt="" width="22" height="8"></td>
                        <td class="money_price buy_price">27.00</td>
                        <td class="money_price">33.00</td>
                    </tr>
                                    <tr>
                        <td class="money_quantity">от 10000</td>
                        <td class="money_icon"><img src="/images/icons/ic-money10000.png" alt="" width="22" height="8"></td>
                        <td class="money_price buy_price">27.50</td>
                        <td class="money_price">32.50</td>
                    </tr>
                                </tbody></table>"""

    res = _parse_ligovka_rate(valid_czk_html)

    assert res == Decimal(30)


async def test_parse_ligovka_rate_corrupted_html():
    corrupted_html = """
    <table class="table_course">
            <tbody>
            <tr class="actions_with_money">
                <td colspan="2"></td>
                <td class="buy_col">Покупка</td>
                <td class="sale_col">Продажа</td>
            </tr>
                                <tr>
                    <td class="money_quantity">от 1</td>
                    <td class="money_icon"><img src="/images/icons/ic-money1.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">73.045</td>
                    <td class="money_price">71.50</td>
                </tr>
                                <tr>
                    <td class="money_quantity">от 1000</td>
                    <td class="money_icon"><img src="/images/icons/ic-money1000.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">75.58</td>
                </tr>
                                <tr>
                    <td class="money_quantity">от 10000</td>
                    <td class="money_icon"><img src="/images/icons/ic-money10000.png" alt="" width="22" height="8"></td>
                    <td class="money_price buy_price">77.456</td>
                    <td class="money_price">79.50</td>
                </tr>
                            </tbody></table>
    """

    with pytest.raises(RuntimeError, match='rates corrupted'):
        _parse_ligovka_rate(corrupted_html)


@pytest.mark.parametrize('payload', [
    '<html></html>',
    '',
])
async def test_parse_ligovka_rate_invalid_html(payload):
    with pytest.raises(RuntimeError, match='rates not found'):
        _parse_ligovka_rate(payload)
