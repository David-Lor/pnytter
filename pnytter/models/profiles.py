import datetime

import pydantic

from .base import BasePnytterModel, NEString

__all__ = ("TwitterProfile",)


class TwitterProfile(BasePnytterModel):
    id: int = pydantic.Field(..., ge=0)
    username: str = NEString
    fullname: str
    biography: str
    joined_datetime: datetime.datetime
