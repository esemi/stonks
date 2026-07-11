"""Stonks telegram bot app."""
import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot_handlers.convert import convert_currency_handler
from app.bot_handlers.details import rate_details_handler
from app.bot_handlers.stonks import current_rates_handler
from app.bot_handlers.welcome import welcome_handler
from app.settings import app_settings

dp = Dispatcher()


async def main() -> None:
    """Telegram bot app runner."""
    bot_instance = Bot(token=app_settings.telegram_token)
    dp.message(welcome_handler, commands=['help', 'start'])
    dp.message(current_rates_handler, commands=['stonks'])
    dp.message(rate_details_handler, commands=['details'])
    dp.message(convert_currency_handler, commands=['convert'])

    await dp.start_polling(bot_instance)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(main())
