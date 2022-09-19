"""Stonks telegram bot app."""
import logging

from aiogram import Bot, Dispatcher, executor

from app.bot_handlers.details import rate_details_handler
from app.bot_handlers.stonks import current_rates_handler
from app.bot_handlers.welcome import welcome_handler
from app.settings import app_settings


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
