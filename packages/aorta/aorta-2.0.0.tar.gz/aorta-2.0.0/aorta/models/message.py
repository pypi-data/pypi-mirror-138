"""Declares :class:`Message`."""
import pydantic

from .messagemetadata import MessageMetadata


class Message(pydantic.BaseModel):
    api_version: str = pydantic.Field(..., alias='apiVersion')
    kind: str = pydantic.Field(...)
    type: str = pydantic.Field(None)
    metadata: MessageMetadata = pydantic.Field(...)
    data: dict = pydantic.Field({})
    spec: dict = pydantic.Field({})
