"""/convert <amount><currency> handler."""
import dataclasses
import logging
import re
from decimal import Decimal
from typing import Optional

from aiogram import types
from prettytable import PrettyTable

from app import currency, storage
from app.bot_handlers.common import log_request
from app.rates_model import CurrencyRates, SummaryRates
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
            text=reply,
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


@dataclasses.dataclass
class ConvertRequest:
    """Request for currency conversion."""

    currency: str
    amount: Decimal


def _parse_convert_request(convert_message: Optional[str]) -> Optional[ConvertRequest]:
    if not convert_message:
        return None

    msg = str(convert_message).strip().lower()
    match_result = re.match(r'([\d.]+)([\s\w$€]+)', msg, re.UNICODE)
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
    if convert_request.currency == currency.RUB:
        message_content: list[str] = []
        for currency_code in app_settings.supported_foreign_currencies:
            conversion_table = _get_conversion_table_from_rub(
                convert_request,
                actual_rates.get_rates(currency_code),
            )
            message_content.append(conversion_table.get_string(border=False))
        response = '\n\n'.join(message_content)

    else:
        conversion_table = _get_conversion_table_to_rub(
            convert_request,
            currency_rates=actual_rates.get_rates(convert_request.currency),
        )
        response = conversion_table.get_string(border=False)

    return response


def _get_conversion_table_to_rub(convert_request: ConvertRequest, currency_rates: CurrencyRates) -> PrettyTable:
    table = PrettyTable(
        field_names=[currency.RUB.upper(), ''],
        align='l',
    )
    table.add_row(['Forex', format_amount(
        round(convert_request.amount * currency_rates.forex),
    )])
    table.add_row(['Cash', format_amount(
        round(convert_request.amount * currency_rates.cash),
    )])
    table.add_row(['Avg', format_amount(
        round(convert_request.amount * currency_rates.avg),
    )])

    if convert_request.currency != currency.CZK:
        table.add_row(['p2p', format_amount(
            round(convert_request.amount * currency_rates.p2p),
        )])

    return table


def _get_conversion_table_from_rub(convert_request: ConvertRequest, currency_rates: CurrencyRates) -> PrettyTable:
    table = PrettyTable(
        field_names=[currency_rates.currency.upper(), ''],
        align='l',
    )
    table.add_row(['Forex', format_amount(
        round(convert_request.amount / currency_rates.forex),
    )])
    table.add_row(['Cash', format_amount(
        round(convert_request.amount / currency_rates.cash),
    )])
    table.add_row(['Avg', format_amount(
        round(convert_request.amount / currency_rates.avg),
    )])

    if currency_rates.currency != currency.CZK:
        table.add_row(['p2p', format_amount(
            round(convert_request.amount / currency_rates.p2p),
        )])

    return table


def format_amount(amount: int) -> str:
    """Format amounts for humans."""
    return '{0:,}'.format(amount).replace(',', ' ')
