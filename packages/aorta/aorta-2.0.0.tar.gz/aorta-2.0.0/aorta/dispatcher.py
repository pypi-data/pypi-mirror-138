"""Declares :class:`Dispatcher`."""
import asyncio
import typing

from .handler import Handler
from .models import Message
from .runner import BaseRunner


class Dispatcher:
    """Dispatches messages to the appropriate handlers."""

    def __init__(self):
        self._handlers = []

    async def dispatch(self,
        runner: BaseRunner,
        message: Message
    ):
        """Collect handlers for incoming message `message` and execute them
        using `runner`.
        """
        await asyncio.gather(*self.run_handlers(runner, message))

    def get_handlers(self, message: Message) -> typing.List[Handler]:
        """Return the list of handlers that listen for the given message."""
        return [x for x in self._handlers if x.can_handle(message)]

    def register(self, handler_class: type, *args, **kwargs) -> None:
        """Register the handler class."""
        self._handlers.append(handler_class(*args, **kwargs))

    def run_handlers(self,
        runner: BaseRunner,
        message: Message
    ) -> typing.List[typing.Awaitable]:
        """Return a list of awaitables that execute the message handler(s)."""
        return [runner.run(x, message) for x in self.get_handlers(message)]
