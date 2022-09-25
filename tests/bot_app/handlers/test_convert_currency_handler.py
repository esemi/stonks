from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.bot_handlers.convert import convert_currency_handler, _parse_convert_request, ConvertRequest


async def test_convert_currency_handler_invalid_request():
    message_mock = AsyncMock(text='invalid convert request')
    expected_message = 'I dont understand'

    await convert_currency_handler(message=message_mock)

    assert message_mock.reply.call_count == 1
    assert expected_message in message_mock.reply.call_args.args[0]


async def test_convert_currency_handler_happy_path():
    message_mock = AsyncMock(text='15000 czk')
    expected_message = 'Conversion result'

    await convert_currency_handler(message=message_mock)

    assert message_mock.reply.call_count == 1
    assert expected_message in message_mock.reply.call_args.args[0]


@pytest.mark.parametrize('message_text, expected_amount, expected_currency', [
    ('15000 czk', Decimal(15000), 'czk'),
    ('15000Kč', Decimal(15000), 'czk'),
    ('15000EuR', Decimal(15000), 'eur'),
    ('150  €  ', Decimal(150), 'eur'),
    ('1.456 usd', Decimal('1.456'), 'usd'),
    ('300 баксов', Decimal('300'), 'usd'),
    ('1.456$', Decimal('1.456'), 'usd'),
    ('45000.45р', Decimal('45000.45'), 'rub'),
    ('45000.45 RUB', Decimal('45000.45'), 'rub'),
    ('45000.45 руб', Decimal('45000.45'), 'rub'),
    ('45000.45 рублей', Decimal('45000.45'), 'rub'),
])
def test_parse_convert_request_valid_request(
    message_text: str,
    expected_amount: Decimal,
    expected_currency: str,
):
    result: ConvertRequest = _parse_convert_request(message_text)

    assert result is not None
    assert result.amount == expected_amount
    assert result.currency == expected_currency


@pytest.mark.parametrize('message_text', [
    '15000sdsdsd',
    '789 AUD',
    '0 BTC',
    '15000',
    'eur',
])
def test_parse_convert_request_invalid_request(message_text: str):
    result = _parse_convert_request(message_text)

    assert result is None
