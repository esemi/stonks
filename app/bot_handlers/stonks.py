"""/stonks handler."""

from aiogram import types
from prettytable import PrettyTable

from app import storage
from app.bot_handlers.common import log_request
from app.settings import app_settings


async def current_rates_handler(message: types.Message) -> None:
    """Display short info about exchange rates."""
    await log_request(message)

    actual_rates = await storage.get_rates()

    table = PrettyTable()
    table.field_names = ['', 'Stonks', 'Gents']
    table.align = 'r'
    for code in app_settings.supported_foreign_currencies:
        table.add_row([
            code.upper(),
            f'{getattr(actual_rates.forex, code):.2f}',
            f'{getattr(actual_rates.cash, code):.2f}',
        ])

    table_content = table.get_string(
        border=False,
    )
    await message.answer(
        text=f'<pre>{table_content}</pre>\n\n<i>{actual_rates.created_at.strftime("%d.%m.%Y %H:%M UTC")}</i>',
        parse_mode='HTML',
    )
