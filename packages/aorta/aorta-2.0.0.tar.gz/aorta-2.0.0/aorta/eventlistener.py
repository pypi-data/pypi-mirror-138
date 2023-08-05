"""Declares :class:`EventListener`."""
import typing

from .handler import Handler
from .models import Message


class EventListener(Handler):
    """A :class:`Handler` implementation that processes messages that
    represent events.
    """
    __module__: str = 'aorta'

    #: A list of tuples specifying the api version and message type
    #: that are accepted by this handler.
    handles: typing.List[typing.Tuple[str, str]] = []

    def can_handle(self, message: Message) -> bool:
        """Return a boolean indicating if the :class:`Handler` knows
        how to process `message`.
        """
        return (message.api_version, message.kind) in self.handles
