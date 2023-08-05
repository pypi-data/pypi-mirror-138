"""Declares :class:`MessageMetadata`."""
import uuid

import pydantic


class MessageMetadata(pydantic.BaseModel):
    message_id: uuid.UUID = pydantic.Field(...,
        alias='messageId'
    )

    correlation_id: uuid.UUID = pydantic.Field(None,
        alias='correlationId'
    )

    published: int = pydantic.Field(...)

    annotations: dict = pydantic.Field({})
    labels: dict = pydantic.Field({})
