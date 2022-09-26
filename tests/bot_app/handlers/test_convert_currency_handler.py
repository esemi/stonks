from decimal import Decimal
from unittest.mock import AsyncMock, Mock

import pytest

from app.bot_handlers.convert import convert_currency_handler, _parse_convert_request, ConvertRequest


async def test_convert_currency_handler_invalid_request():
    message_mock = AsyncMock()
    message_mock.get_args = Mock(return_value='invalid convert request')
    expected_message = 'I dont understand'

    await convert_currency_handler(message=message_mock)

    assert message_mock.reply.call_count == 1
    assert expected_message in message_mock.reply.call_args.kwargs['text']


async def test_convert_currency_handler_to_rub(fixture_filled_rates):
    message_mock = AsyncMock()
    message_mock.get_args = Mock(return_value='15000 czk')

    await convert_currency_handler(message=message_mock)

    assert message_mock.reply.call_count == 1
    assert 'RUB' in message_mock.reply.call_args.kwargs['text']


async def test_convert_currency_handler_from_rub(fixture_filled_rates):
    message_mock = AsyncMock()
    message_mock.get_args = Mock(return_value='15000 руб')

    await convert_currency_handler(message=message_mock)

    assert message_mock.reply.call_count == 1
    assert 'CZK' in message_mock.reply.call_args.kwargs['text']
    assert 'EUR' in message_mock.reply.call_args.kwargs['text']
    assert 'USD' in message_mock.reply.call_args.kwargs['text']


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
    None,
])
def test_parse_convert_request_invalid_request(message_text: str):
    result = _parse_convert_request(message_text)

    assert result is None
