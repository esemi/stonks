"""/help handler."""

from aiogram import types

from app.bot_handlers.common import log_request


async def welcome_handler(message: types.Message) -> None:
    """Display bot usage."""
    await log_request(message)

    reply = '\n'.join((
        "Hi! I'm Stonks & Gents Bot!",
        'And I know about currency exchange rates ;)',
        '<b>Usage</b>:',
        '/stonks - display exchange rates;',
        '/details - display details exchange rates info;',
        '/convert &lt;amount&gt;&lt;currency&gt; - convert currency from/to RUB;',
        '/help - display bot help.',
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
