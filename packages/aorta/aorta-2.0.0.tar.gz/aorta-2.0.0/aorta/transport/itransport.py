"""Declares :class:`ITransport`."""
import logging

from ..models import Message


class ITransport:
    """Declares the interface for all transport implementations."""
    logger: logging.Logger = logging.getLogger('uvicorn')

    async def send(self, message: Message):
        raise NotImplementedError
