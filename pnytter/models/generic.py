import urllib.parse

import pydantic

from .base import BasePnytterModel, NEString

__all__ = ("TwitterURL",)

HTTPS = "https://"


class TwitterURL(BasePnytterModel):
    twitter_url: pydantic.HttpUrl
    nitter_path: str = NEString

    @classmethod
    def from_nitter_path(cls, path: str) -> "TwitterURL":
        # noinspection PyTypeChecker
        return cls(
            twitter_url=cls._nitter_path_to_twitter_url(path),
            nitter_path=path,
        )

    @staticmethod
    def _nitter_path_to_twitter_url(path: str) -> str:
        # path example:
        #   /pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500
        twitter_url = path.split("/pic/")[-1]
        twitter_url = urllib.parse.unquote(twitter_url)
        if not twitter_url.startswith(HTTPS):
            twitter_url = HTTPS + twitter_url
        return twitter_url
