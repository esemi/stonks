"""Handlers common utils."""

import logging

from aiogram import types

from app import storage


async def log_request(message: types.Message) -> None:
    """Log bot request for stats."""
    chat_name = message.chat.id
    if 'username' in message.chat:
        chat_name = f'private-{message.chat.username}'
    if 'title' in message.chat:
        chat_name = f'channel-{message.chat.title}'

    await storage.inc_stats(
        message.get_command(),
        chat_name,
    )

    logging.info('{0} call: username={1} from chat={2}'.format(
        message.get_command(),
        message.from_user.username,
        chat_name,
    ))
