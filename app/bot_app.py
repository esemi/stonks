"""Stonks telegram bot app."""
import logging

from aiogram import Bot, Dispatcher, executor, types
from prettytable import PrettyTable

from app import storage
from app.settings import app_settings


async def welcome_handler(message: types.Message) -> None:
    """Display bot usage."""
    await _save_stat(message)

    reply = '\n'.join((
        "Hi! I'm Stonks & Gents Bot!",
        'And I know about currency exchange rates ;)',
        '<b>Usage</b>:',
        '/stonks - display exchange rates;',
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
    """Display current exchange rates for cash and forex sources."""
    await _save_stat(message)

    actual_rates = await storage.get_rates()

    table = PrettyTable()
    table.field_names = ['', 'Stonks', 'Gents', 'Diff']
    table.align = 'r'
    for code in app_settings.supported_currencies:
        stonks_rate = getattr(actual_rates.forex, code)
        gents_rate = getattr(actual_rates.cash, code)
        diff = gents_rate - stonks_rate
        table.add_row([
            code.upper(),
            '{0:.2f}'.format(stonks_rate),
            '{0:.2f}'.format(gents_rate),
            '{0:.2f}%'.format(diff / stonks_rate * 100),
        ])

    table_content = table.get_string(
        border=False,
    )
    await message.answer(
        text=f'<pre>{table_content}</pre>\n\n<i>{actual_rates.created_at.strftime("%d.%m.%Y %H:%M UTC")}</i>',
        parse_mode='HTML',
        disable_web_page_preview=True,
    )


async def _save_stat(message: types.Message) -> None:
    await storage.inc_stats(
        message.get_command(),
        message.chat.id,
    )


def main() -> None:
    """Telegram bot app runner."""
    bot = Bot(
        token=app_settings.telegram_token,
        timeout=app_settings.http_timeout,
    )

    router = Dispatcher(bot)
    router.register_message_handler(welcome_handler, commands=['help'])
    router.register_message_handler(current_rates_handler, commands=['stonks'])
    executor.start_polling(router, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    main()
