import datetime
from typing import Union


class Utils:
    @staticmethod
    def clean_username(username: str) -> str:
        """Clean a Twitter profile username, by removing the leading '@' if present."""
        if username and username[0] == "@":
            username = username[1:]
        return username

    @staticmethod
    def parse_date(s: Union[str, datetime.date]) -> datetime.date:
        if isinstance(s, str):
            s = datetime.date.fromisoformat(s)
        return s


class Const:
    class Nitter:
        tweets_per_page = 20
