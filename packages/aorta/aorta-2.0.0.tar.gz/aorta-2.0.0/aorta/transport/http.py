# flake8: noqa
"""Declares :class:`EventListenerEndpoint`."""
import collections
import inspect
import typing

import fastapi
from unimatrix.ext import webapi

from ..models import Envelope
from ..models import Message
from ..models.google import MessagePublished


class MessageReceiver(webapi.Service):

    #: The list of parsers that parse incoming messages to a common format.
    parsers: typing.List[object] = [
        MessagePublished,
    ]

    @classmethod
    def add_adapter(self, cls: Envelope) -> None:
        """Add a new adapter to the :class:`MessageReceiver`."""
        self.parsers.insert(0, cls)

    async def command(self, request: fastapi.Request, dto: Envelope):
        """Issue a command for further processing."""
        print(dto.get_message())

    async def event(self, request: fastapi.Request, dto: Envelope):
        """Receive an event over HTTP."""
        print(dto.get_message())

    def setup_routes(self, path: str) -> None:
        self.add_api_route(
            name='command',
            path='/commands',
            endpoint=self._update_signature(self.command),
            status_code=202,
            summary='command',
            methods=['POST'],
            operation_id='issue',
        )
        self.add_api_route(
            name='event',
            path='/events',
            endpoint=self._update_signature(self.event),
            status_code=202,
            summary='event',
            methods=['POST'],
            operation_id='publish',
        )

    def _update_signature(self, handler: typing.Callable):
        async def f(*args, **kwargs):
            return await handler(*args, **kwargs)

        sig = inspect.signature(handler)
        params = collections.OrderedDict(sig.parameters.items())
        params['dto'] = inspect.Parameter(
            name='dto',
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=typing.Union[tuple(self.parsers)]
        )

        f.__signature__ = sig.replace(parameters=list(params.values()))
        return f
