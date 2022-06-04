"""Stonks telegram bot app."""
import logging

from aiogram import Bot, Dispatcher, executor, types

from app.settings import app_settings


async def welcome_handler(message: types.Message):
    """Display bot usage."""
    # todo test
    await message.reply('Hi! I\'m Stonks&Gents Bot!\nTouch me by /stonks command.')


async def current_rates_handler(message: types.Message):
    """Display current exchange rates for cash and forex sources."""
    # todo impl
    # todo test
    await message.answer(
        'todo current rates here',
    )


def main():
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
