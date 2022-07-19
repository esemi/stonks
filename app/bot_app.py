"""Stonks telegram bot app."""
import logging
from decimal import Decimal
from typing import Tuple

from aiogram import Bot, Dispatcher, executor, types
from prettytable import PrettyTable

from app import storage
from app.rates_model import SummaryRates
from app.settings import app_settings


async def welcome_handler(message: types.Message) -> None:
    """Display bot usage."""
    await _log_request(message)

    reply = '\n'.join((
        "Hi! I'm Stonks & Gents Bot!",
        'And I know about currency exchange rates ;)',
        '<b>Usage</b>:',
        '/stonks - display exchange rates;',
        '/details - display details exchange rates info;',
        '/help - display bot help;',
        '',
        '<i><b>Stonks</b></i> - rate on <a href="https://finance.yahoo.com/currencies" target="_blank">forex</a>,',
        '<i><b>Gents</b></i> - rate on <a href="https://blagodatka.ru/"  target="_blank">currency exchange point</a>.',
        '',
        '<a href="https://github.com/esemi/stonks" target="_blank">source code</a>',
    ))
    await message.reply(
        reply,
        parse_mode='HTML',
        disable_web_page_preview=True,
    )


async def current_rates_handler(message: types.Message) -> None:
    """Display short info about exchange rates."""
    await _log_request(message)

    actual_rates = await storage.get_rates()

    table = PrettyTable()
    table.field_names = ['', 'Stonks', 'Gents']
    table.align = 'r'
    for code in app_settings.supported_currencies:
        table.add_row([
            code.upper(),
            '{0:.2f}'.format(getattr(actual_rates.forex, code)),
            '{0:.2f}'.format(getattr(actual_rates.cash, code)),
        ])

    table_content = table.get_string(
        border=False,
    )
    await message.answer(
        text=f'<pre>{table_content}</pre>\n\n<i>{actual_rates.created_at.strftime("%d.%m.%Y %H:%M UTC")}</i>',
        parse_mode='HTML',
    )


async def rate_details_handler(message: types.Message) -> None:
    """Display detailed exchange rates for cash and forex sources."""
    await _log_request(message)

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
            field_names=[code.upper(), 'Rate'],
            align='l',
        )
        forex_rate, cash_rate, avg_rate = _calculate_currency_rates(
            actual_rates=actual_rates,
            currency_code=code,
        )
        table.add_row(['Forex', forex_rate])
        table.add_row(['Cash', cash_rate])
        table.add_row(['Avg', avg_rate])

        message_content.append(table.get_string(border=True))
    return '\n\n'.join(message_content)


def _calculate_currency_rates(actual_rates: SummaryRates, currency_code: str) -> Tuple[str, str, str]:
    forex_rate = getattr(actual_rates.forex, currency_code)
    cash_rate = getattr(actual_rates.cash, currency_code)
    cash_diff = (cash_rate - forex_rate) / forex_rate * 100
    avg_rate = (cash_rate + forex_rate) / 2
    avg_diff = (avg_rate - forex_rate) / forex_rate * 100
    return (
        '{0:.4f}'.format(forex_rate),
        '{0:.4f} ({1}{2:.2f}%)'.format(
            cash_rate,
            _return_number_sign(cash_diff),
            cash_diff,
        ),
        '{0:.4f} ({1}{2:.2f}%)'.format(
            avg_rate,
            _return_number_sign(avg_diff),
            avg_diff,
        ),
    )


async def _log_request(message: types.Message) -> None:
    await storage.inc_stats(
        message.get_command(),
        message.chat.username,
    )

    logging.info('{0} call: username={1} from chat={2}'.format(
        message.get_command(),
        message.from_user.username,
        message.chat.username,
    ))


def _return_number_sign(amount: Decimal) -> str:
    return '+' if amount >= 0 else '-'


def main() -> None:
    """Telegram bot app runner."""
    bot = Bot(
        token=app_settings.telegram_token,
        timeout=app_settings.http_timeout,
    )

    router = Dispatcher(bot)
    router.register_message_handler(welcome_handler, commands=['help'])
    router.register_message_handler(current_rates_handler, commands=['stonks'])
    router.register_message_handler(rate_details_handler, commands=['details'])
    executor.start_polling(router, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    main()
