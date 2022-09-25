"""/convert <amount><currency> handler."""
import dataclasses
import logging
import re
from decimal import Decimal
from typing import Optional

from aiogram import types

from app.bot_handlers.common import log_request
from app.settings import app_settings


async def convert_currency_handler(message: types.Message) -> None:
    """Convert currency."""
    await log_request(message)

    convert_request = _parse_convert_request(message.text)
    if not convert_request:
        logging.warning('invalid convert call: {0} from chat={1}'.format(
            message.text,
            message.from_user.username,
        ))
        reply = '\n'.join((
            'I dont understand =(',
            '<b>Usage</b>:',
            '<pre>/convert 15000 czk</pre>',
            '<pre>/convert 8000 kč</pre>',
            '<pre>/convert 45000 rub</pre>',
            '<pre>/convert 1500р</pre>',
            '<pre>/convert 3000 eur</pre>',
        ))
        await message.reply(
            reply,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )


#     todo impl converter
#     todo impl converter display
#     todo test


@dataclasses.dataclass
class ConvertRequest:
    """Request for currency conversion."""

    currency: str
    amount: Decimal


def _parse_convert_request(convert_message: str) -> Optional[ConvertRequest]:
    match_result = re.match(r'([\d.]+)([\s\w$€]+)', convert_message.strip().lower(), re.UNICODE)
    if not match_result:
        return None

    match_groups = match_result.groups()
    amount = Decimal(match_groups[0].strip())
    currency = match_groups[1].strip().lower()

    if currency not in app_settings.currency_aliases:
        return None

    return ConvertRequest(
        currency=app_settings.currency_aliases[currency],
        amount=amount,
    )
