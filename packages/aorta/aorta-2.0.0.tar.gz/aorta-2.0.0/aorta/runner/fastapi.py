"""Declares :class:`FastAPIRunner`."""
import typing

try:
    from fastapi import Request
    from fastapi.dependencies.utils import get_dependant
    from fastapi.dependencies.utils import get_parameterless_sub_dependant
    from fastapi.dependencies.utils import solve_dependencies
except ImportError:
    Request = None

from ..models import Message
from .base import BaseRunner


class FastAPIRunner(BaseRunner):
    """A :class:`~aorta.BaseRunner` implementation that uses the :mod:`fastapi`
    dependency injection framework.
    """

    def __init__(self, request: Request):
        if Request is None:
            raise ImportError(
                "The fastapi module must be installed to use FastAPIRunner"
            )
        self.request = request

    async def run(self,
        handler: typing.Callable,
        message: Message,
        *args, **kwargs
    ) -> None:
        """Run callable `handler` with the given parameters."""
        dependant = get_dependant(path='/', call=handler.handle)
        values, *_ = await solve_dependencies(
            request=self.request,
            dependant=dependant,
            body=None,
            dependency_overrides_provider=None
        )
        await dependant.call(message, **values)
