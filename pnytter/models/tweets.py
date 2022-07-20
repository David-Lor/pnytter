import datetime

from .base import BasePnytterModel, NEString, PosInt

__all__ = ("TwitterTweet",)


class TwitterTweet(BasePnytterModel):
    tweet_id: int = PosInt
    author: str = NEString
    created_on: datetime.datetime
    text: str
