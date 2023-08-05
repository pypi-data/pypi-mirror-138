"""Declares :class:`Handler`."""
import typing

from .models import Message
from .node import Node


class Handler(Node):
    """Handles an incoming message using the :meth:`handle()` method."""
    __module__: str = 'aorta'

    def __init__(self):
        self.logger.debug(
            "Initializing message handler %s",
            type(self).__name__
        )

    async def handle(self, message: Message, *args, **kwargs):
        """Invoked for each incoming message that matches the handlers'
        criteria.
        """
        raise NotImplementedError
