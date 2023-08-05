"""Declares :class:`EventPublisher`."""
import typing
import uuid

from unimatrix.lib import timezone

from .models import Message
from .models import MessageMetadata
from .transport import ITransport


class EventPublisher:
    """Provides an interface to published event messages."""
    __module__: str = 'aorta'

    def __init__(self, transport: ITransport):
        """Initialize a new :class:`EventPublisher`.

        Args:
            transport: a :class:`ITransport` implementation that is
                used to relay messages.
        """
        self._transport = transport

    async def publish(self,
        dto: typing.Union[dict, Message],
        correlation_id: str = None
    ):
        """Publish an event to the upstream peer."""
        metadata = {
            'messageId': uuid.uuid4(),
            'correlationId': correlation_id,
            'published': timezone.now()
        }
        if not isinstance(dto, Message):
            dto['type'] = "unimatrixone.io/event"
            dto = Message(metadata=metadata, **dto)
        await self._transport.send(dto)
