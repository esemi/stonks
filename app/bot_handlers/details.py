"""/details handler."""

from decimal import Decimal

from aiogram import types
from prettytable import PrettyTable

from app import storage
from app.bot_handlers.common import log_request
from app.rates_model import SummaryRates
from app.settings import app_settings


async def rate_details_handler(message: types.Message) -> None:
    """Display detailed exchange rates for cash and forex sources."""
    await log_request(message)

    actual_rates = await storage.get_rates()
    prepared_message = _prepare_details_table(actual_rates)

    await message.answer(
        text=f'<pre>{prepared_message}</pre>\n\n<i>{actual_rates.created_at.strftime("%d.%m.%Y %H:%M UTC")}</i>',
        parse_mode='HTML',
    )


def _prepare_details_table(actual_rates: SummaryRates) -> str:
    message_content: list[str] = []
    for code in app_settings.supported_currencies:
        table = PrettyTable(
            field_names=[code.upper(), ''],
            align='l',
        )
        _fill_currency_table(
            table=table,
            actual_rates=actual_rates,
            currency_code=code,
        )
        message_content.append(table.get_string(border=False))

    return '\n\n'.join(message_content)


def _fill_currency_table(table: PrettyTable, actual_rates: SummaryRates, currency_code: str) -> None:
    forex_rate = getattr(actual_rates.forex, currency_code)
    bloomberg_rate = getattr(actual_rates.bloomberg, currency_code)
    cash_rate = getattr(actual_rates.cash, currency_code)
    p2p_rate = getattr(actual_rates.p2p, currency_code)
    avg_rate = (cash_rate + forex_rate) / 2

    table.add_row(['Forex', '{0:.4f}'.format(forex_rate)])
    table.add_row(['Bloomberg', _format_rate_with_diff(bloomberg_rate, forex_rate)])
    table.add_row(['Cash', _format_rate_with_diff(cash_rate, forex_rate)])
    table.add_row(['Avg', _format_rate_with_diff(avg_rate, forex_rate)])
    if currency_code != 'czk':
        table.add_row(['p2p', _format_rate_with_diff(p2p_rate, forex_rate)])


def _format_rate_with_diff(rate: Decimal, base_rate: Decimal) -> str:
    diff = (rate - base_rate) / base_rate * 100
    return '{0:.4f} ({1}{2:.1f}%)'.format(
        rate,
        _return_number_sign(diff),
        abs(diff),
    )


def _return_number_sign(amount: Decimal) -> str:
    return '+' if amount >= 0 else '-'
