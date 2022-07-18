import re
import datetime

import pydantic

from .base import BasePnytterModel, NEString, PosInt
from .generic import TwitterURL

__all__ = ("TwitterProfile",)


class TwitterProfile(BasePnytterModel):
    class Stats(BasePnytterModel):
        tweets: int = PosInt
        following: int = PosInt
        followers: int = PosInt
        likes: int = PosInt

        @pydantic.validator("*", pre=True)
        def _clear_string(cls, v):
            if isinstance(v, str):
                v = re.sub("[^0-9]", "", v)
            return v

    class Pictures(BasePnytterModel):
        profile: TwitterURL
        banner: TwitterURL

    id: int = pydantic.Field(..., ge=0)
    username: str = NEString
    fullname: str
    biography: str
    verified: bool = False
    joined_datetime: datetime.datetime
    stats: Stats
    pictures: Pictures
