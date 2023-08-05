# pylint: skip-file
import ioc

from .commandhandler import CommandHandler
from .dispatcher import Dispatcher
from .eventlistener import EventListener
from .eventpublisher import EventPublisher
from .handler import Handler
from .runner import BaseRunner
from .runner import FastAPIRunner
from . import models
from . import transport


__all__ = [
    'models',
    'publish',
    'transport',
    'Dispatcher',
    'EventListener',
    'FastAPIRunner',
]


_issuer = ioc.require('CommandIssuer')
_publisher = ioc.require('EventPublisher')


async def issue(name: str, params: dict, version: str = 'v1') -> None:
    """Issue a command using the default command issuer."""
    await _issuer.issue({
        'apiVersion': version,
        'kind': name,
        'spec': params
    })


async def publish(name: str, params: dict, version: str = 'v1') -> None:
    """Publishes an event using the default event publisher."""
    await _publisher.publish({
        'apiVersion': version,
        'kind': name,
        'data': params
    })


def register(handler: Handler):
    pass
