import datetime

from .base import BasePnytterModel, BasePnytterStats, NEString, PosInt

__all__ = ("TwitterTweet",)


class TwitterTweet(BasePnytterModel):

    class Stats(BasePnytterStats):
        comments: int = PosInt
        retweets: int = PosInt
        quotes: int = PosInt
        likes: int = PosInt

    tweet_id: int = PosInt
    author: str = NEString
    created_on: datetime.datetime
    text: str
    stats: Stats
