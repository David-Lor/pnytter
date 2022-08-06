import datetime

import pydantic

from .base import BasePnytterModel, BasePnytterStats, NEString, PosInt

__all__ = ("TwitterTweet",)


class TwitterTweet(BasePnytterModel):

    class Stats(BasePnytterStats):
        comments: int = PosInt
        retweets: int = PosInt
        quotes: int = PosInt
        likes: int = PosInt

        @pydantic.validator("*", pre=True, allow_reuse=True)
        def _empty_string_as_zero(cls, v):
            """If a string is empty, set its value to 0."""
            if isinstance(v, str) and not v.strip():
                v = 0
            return v

    tweet_id: int = PosInt
    author: str = NEString
    created_on: datetime.datetime
    text: str
    stats: Stats
