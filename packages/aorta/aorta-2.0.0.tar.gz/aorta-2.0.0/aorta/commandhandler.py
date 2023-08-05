"""Declares :class:`CommandHandler`."""
from .handler import Handler
from .models import Message


class CommandHandler(Handler):
    """A :class:`Handler` implementation that handles incoming messages that
    represent commands.
    """

    async def handle(self, message: Message, *args, **kwargs):
        """Invoked for each incoming message that matches the handlers'
        criteria.
        """
        raise NotImplementedError
