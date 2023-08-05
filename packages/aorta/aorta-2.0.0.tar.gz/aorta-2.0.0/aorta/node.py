"""Declares :class:`Node`."""
import logging

import ioc


class Node:
    """Represents a node in a network that receives and produces messages."""
    logger: logging.Logger = logging.getLogger('uvicorn')

    @property
    def _issuer(self):
        return ioc.require('CommandIssuer')

    @property
    def _publisher(self):
        return ioc.require('EventPublisher')

    async def issue(self, name: str, params: dict, version: str = 'v1'):
        """Issue a command using the default command issuer."""
        await self._issuer.issue({
            'apiVersion': version,
            'kind': name,
            'spec': params
        })

    async def publish(self, name: str, params: dict, version: str = 'v1'):
        """Publishes an event using the default event publisher."""
        await self._publisher.publish({
            'apiVersion': version,
            'kind': name,
            'data': params
        })
