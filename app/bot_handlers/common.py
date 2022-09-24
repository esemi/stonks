"""Handlers common utils."""

import logging

from aiogram import types

from app import storage


async def log_request(message: types.Message) -> None:
    """Log bot request for stats."""
    await storage.inc_stats(
        message.get_command(),
        message.chat.username,
    )

    logging.info('{0} call: username={1} from chat={2}'.format(
        message.get_command(),
        message.from_user.username,
        message.chat.username,
    ))
