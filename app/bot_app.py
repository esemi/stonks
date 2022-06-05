"""Stonks telegram bot app."""
import logging

from aiogram import Bot, Dispatcher, executor, types
from prettytable import PrettyTable

from app import storage
from app.settings import app_settings


async def welcome_handler(message: types.Message) -> None:
    """Display bot usage."""
    await message.reply("Hi! I'm Stonks&Gents Bot!\nTouch me by /stonks command.")


async def current_rates_handler(message: types.Message) -> None:
    """Display current exchange rates for cash and forex sources."""
    actual_rates = await storage.get_rates()

    table = PrettyTable()
    table.field_names = ['', 'Stonks', 'Gents', 'Diff']
    for code in app_settings.supported_currencies:
        stonks_rate = getattr(actual_rates.forex, code)
        gents_rate = getattr(actual_rates.cash, code)
        diff = gents_rate - stonks_rate
        table.add_row([
            f'{code.upper()}.RUB',
            '{0:.2f}'.format(stonks_rate),
            '{0:.2f}'.format(gents_rate),
            '{0:.2f}%'.format(diff / stonks_rate * 100),
        ])

    await message.answer(
        text=f'{actual_rates.created_at.strftime("%d.%m.%Y %H:%M UTC")}\n<pre>{table}</pre>',
        parse_mode='HTML',
        disable_web_page_preview=True,
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
