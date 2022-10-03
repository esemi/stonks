"""/details handler."""

from decimal import Decimal

from aiogram import types
from prettytable import PrettyTable

from app import currency, storage
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
    for code in app_settings.supported_foreign_currencies:
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
    currency_rates = actual_rates.get_rates(currency_code)

    table.add_row(['Moex', _format_rate_with_diff(currency_rates.moex, currency_rates.forex)])
    table.add_row(['Forex', '{0:.4f}'.format(currency_rates.forex)])
    table.add_row(['Cash', _format_rate_with_diff(currency_rates.cash, currency_rates.forex)])
    table.add_row(['Avg', _format_rate_with_diff(currency_rates.avg, currency_rates.forex)])
    if currency_code != currency.CZK:
        table.add_row(['p2p', _format_rate_with_diff(currency_rates.p2p, currency_rates.forex)])


def _format_rate_with_diff(rate: Decimal, base_rate: Decimal) -> str:
    diff = (rate - base_rate) / base_rate * Decimal(100)
    if diff < Decimal('0.1'):
        diff = Decimal(0)
    return '{0:.4f} {1}{2:.1f}%'.format(
        rate,
        _return_number_sign(diff),
        abs(diff),
    )


def _return_number_sign(amount: Decimal) -> str:
    if not amount:
        return ''
    return '+' if amount >= 0 else '-'
