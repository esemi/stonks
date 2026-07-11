"""Handlers common utils."""

import logging

from aiogram import types


def _get_command(message: types.Message) -> str:
    return (message.text or '').split(maxsplit=1)[0]


async def log_request(message: types.Message) -> None:
    """Log bot request for stats."""
    chat_name = str(message.chat.id)
    if message.chat.username:
        chat_name = f'private-{message.chat.username}'
    if message.chat.title:
        chat_name = f'channel-{message.chat.title}'

    command = _get_command(message)
    logging.info(f'{command} call: username={message.from_user.username} from chat={chat_name}')  # type:ignore
