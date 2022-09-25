"""/convert <amount><currency> handler."""
import dataclasses
import logging
import re
from decimal import Decimal
from typing import Optional

from aiogram import types
from prettytable import PrettyTable

from app import storage, currency
from app.bot_handlers.common import log_request
from app.rates_model import SummaryRates
from app.settings import app_settings


async def convert_currency_handler(message: types.Message) -> None:
    """Convert currency."""
    await log_request(message)

    convert_request = _parse_convert_request(message.get_args())
    if not convert_request:
        logging.warning('invalid convert call: "{0}" from chat={1}'.format(
            message.text,
            message.from_user.username,
        ))
        reply = '\n'.join((
            'I dont understand =(',
            '<b>Usage</b>:',
            '<pre>/convert 15000 крон</pre>',
            '<pre>/convert 8000 czk</pre>',
            '<pre>/convert 1500р</pre>',
            '<pre>/convert 3000 eur</pre>',
        ))
        await message.reply(
            reply,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
        return

    actual_rates = await storage.get_rates()
    prepared_message = _prepare_conversion_table(actual_rates, convert_request)

    await message.reply(
        text=f'<pre>{prepared_message}</pre>',
        parse_mode='HTML',
    )


#     todo impl converter


@dataclasses.dataclass
class ConvertRequest:
    """Request for currency conversion."""

    currency: str
    amount: Decimal


def _parse_convert_request(convert_message: Optional[str]) -> Optional[ConvertRequest]:
    if not convert_message:
        return None
    match_result = re.match(r'([\d.]+)([\s\w$€]+)', convert_message.strip().lower(), re.UNICODE)
    if not match_result:
        return None

    match_groups = match_result.groups()
    amount = Decimal(match_groups[0].strip())
    parsed_currency = match_groups[1].strip().lower()

    if parsed_currency not in app_settings.currency_aliases:
        return None

    return ConvertRequest(
        currency=app_settings.currency_aliases[parsed_currency],
        amount=amount,
    )


def _prepare_conversion_table(actual_rates: SummaryRates, convert_request: ConvertRequest) -> str:
    message_content: list[str] = []
    if convert_request.currency == currency.RUB:
        # todo impl
        ...

    else:
        message_content.append('{0} -> RUB'.format(convert_request.currency.upper()))
        conversion_table = _get_conversion_table(convert_request, actual_rates)
        message_content.append(conversion_table)

    return '\n\n'.join(message_content)


def _get_conversion_table(convert_request: ConvertRequest, actual_rates: SummaryRates) -> str:
    forex_rate = getattr(actual_rates.forex, convert_request.currency)
    cash_rate = getattr(actual_rates.cash, convert_request.currency)
    p2p_rate = getattr(actual_rates.p2p, convert_request.currency)
    avg_rate = (cash_rate + forex_rate) / 2

    table.add_row(['Forex', '{0:.4f}'.format(forex_rate)])
    table.add_row(['Cash', _format_rate_with_diff(cash_rate, forex_rate)])
    table.add_row(['Avg', _format_rate_with_diff(avg_rate, forex_rate)])
    if currency_code != 'czk':
        table.add_row(['p2p', _format_rate_with_diff(p2p_rate, forex_rate)])
