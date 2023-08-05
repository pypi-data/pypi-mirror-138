"""Declares :class:`BaseRunner`."""
import typing

from ..models import Message


class BaseRunner:
    """The base class for all runner implementations.

    A runner is a class that sets up the execution context and invokes a
    message handler.
    """

    async def run(self,
        handler: typing.Callable,
        message: Message,
        *args, **kwargs
    ) -> None:
        """Run callable `handler` with the given parameters."""
        raise NotImplementedError("Subclasses must override this method.")
