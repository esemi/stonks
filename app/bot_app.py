"""Stonks telegram bot app."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from app.bot_handlers.convert import convert_currency_handler
from app.bot_handlers.details import rate_details_handler
from app.bot_handlers.stonks import current_rates_handler
from app.bot_handlers.welcome import welcome_handler
from app.settings import app_settings

dp = Dispatcher()


async def main() -> None:
    """Telegram bot app runner."""
    bot_instance = Bot(
        token=app_settings.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp.message.register(welcome_handler, Command('help', 'start'))
    dp.message.register(current_rates_handler, Command('stonks'))
    dp.message.register(rate_details_handler, Command('details'))
    dp.message.register(convert_currency_handler, Command('convert'))

    await dp.start_polling(bot_instance)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(main())
