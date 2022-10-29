import datetime
from typing import Optional

import pydantic

from .base import BasePnytterModel, BasePnytterStats, NEString, PosInt
from .generic import TwitterURL

__all__ = ("TwitterProfile",)


class TwitterProfile(BasePnytterModel):

    class Stats(BasePnytterStats):
        tweets: int = PosInt
        following: int = PosInt
        followers: int = PosInt
        likes: int = PosInt

    class Pictures(BasePnytterModel):
        profile: Optional[TwitterURL] = None
        banner: Optional[TwitterURL] = None

    id: Optional[int] = pydantic.Field(None, ge=0)
    username: str = NEString
    fullname: str
    biography: str
    verified: bool = False
    joined_datetime: datetime.datetime
    stats: Stats
    pictures: Pictures
