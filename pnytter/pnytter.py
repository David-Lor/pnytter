import random
import datetime
from typing import List, Collection, Optional, Union, Generator

import pydantic
import requests
from urljoin import url_path_join

from .nitter_parser import NitterParser
from .models import TwitterProfile, TwitterTweet
from .utils import Utils

__all__ = ("Pnytter",)


class Pnytter(pydantic.BaseModel):

    nitter_instances: Union[List[pydantic.AnyHttpUrl], pydantic.AnyHttpUrl] = pydantic.Field(..., min_items=1)
    """List of the Nitter instances to use. Each instance must be given as the base URL of the Nitter server.
    At least one instance is required. Instances may be repeated for increasing their chances."""

    beautifulsoup_parser: str = "html.parser"
    """BeautifulSoup parser to use for parsing Nitter's HTML."""

    request_timeout: float = pydantic.Field(default=10, ge=0)
    """Timeout in seconds for HTTP requests."""

    @pydantic.validator("nitter_instances")
    def _nitter_instances_single_to_list(cls, v):
        if not isinstance(v, list):
            v = [v]
        return v

    @property
    def nitter_instances_unique(self):
        return set(str(instance) for instance in self.nitter_instances)

    def _get_random_nitter_instance(self) -> str:
        """Retrieve a random Nitter instance URL from the 'nitter_instances' list."""
        return random.choice(self.nitter_instances)

    def _raw_request(
            self,
            method: str,
            url: str,
            params: Optional[dict],
            ignore_statuscodes: Collection[int]
    ) -> str:
        """Method for performing an HTTP request, and returning the response body as string.
        This method can be overriden by the code that uses Pnytter, if required."""
        r = requests.request(
            method=method,
            url=url,
            params=params,
            timeout=self.request_timeout,
        )
        if r.status_code not in ignore_statuscodes:
            r.raise_for_status()
        return r.text

    def _request_nitter(
            self,
            endpoint: str,
            params: Optional[dict] = None,
            method: str = "GET",
            ignore_statuscodes: Optional[Collection[int]] = None,
            nitter_instance: Optional[str] = None,
    ) -> str:
        """Perform an HTTP request to Nitter, for the given endpoint.
        This method chooses a random Nitter instance to use for the request."""
        nitter_instance = nitter_instance if nitter_instance else self._get_random_nitter_instance()
        url = url_path_join(nitter_instance, endpoint)

        return self._raw_request(
            method=method,
            url=url,
            params=params,
            ignore_statuscodes=ignore_statuscodes or (),
        )

    def find_user(
            self,
            username: str
    ) -> Optional[TwitterProfile]:
        """Get the information of a Twitter user, given its public username. If the profile does not exist, return None.
        :param username: Twitter profile username (example: "@jack")
        """
        username = Utils.clean_username(username)
        html = self._request_nitter(
            endpoint=username,
            ignore_statuscodes=[404],
        )
        return NitterParser(
            parser=self.beautifulsoup_parser,
            html=html,
        ).get_profile()

    def get_user_tweets(
            self,
            username: str,
            filter_from: Optional[Union[datetime.date, str]],
            filter_to: Optional[Union[datetime.date, str]],
    ) -> Generator[TwitterTweet, None, None]:
        """Get all the tweets from a username. Basic retweets (RTs without a custom comment) will not be returned.
        The found tweets are yield as a generator, for each page of results fetched from Nitter.
        :param username: username of the profile to search tweets from.
        :param filter_from: filter from a date (inclusive). Given as datetime.date or a string with format 'YYYY-MM-DD'.
        :param filter_to: filter until a date (exclusive). Given as datetime.date or a string with format 'YYYY-MM-DD'.
        :return:
        """
        username = Utils.clean_username(username)
        filter_from = Utils.parse_date(filter_from)
        filter_to = Utils.parse_date(filter_to)

        params = {
            "f": "tweets",
            "e-nativeretweets": "on",  # exclude Retweets
            "since": filter_from.isoformat() if filter_from else "",
            "until": filter_to.isoformat() if filter_to else "",
        }
        endpoint_base = f"{username}/search"
        endpoint_params = ""

        while True:
            html = self._request_nitter(
                endpoint=endpoint_base + endpoint_params,
                params=params,
            )

            parser = NitterParser(
                parser=self.beautifulsoup_parser,
                html=html,
            )
            tweets = parser.get_tweets_from_searchpage()
            if not tweets:
                return

            yield tweets

            endpoint_params = parser.get_searchpage_nextpage_params()
            if not endpoint_params:
                return

    def get_user_tweets_list(self, *args, **kwargs) -> List[TwitterTweet]:
        """Call the get_user_tweets() method, but returning a list with all the found tweets. Refer to the mentioned
        method documentation for more details and the list of arguments supported."""
        tweets = list()
        for tweets_page in self.get_user_tweets(*args, **kwargs):
            tweets.extend(tweets_page)

        return tweets

    def get_tweet(
            self,
            tweet_id: Union[str, int],
            search_all_instances: bool = False,
    ) -> Optional[TwitterTweet]:
        """Get a single Tweet by its id. Return the TwitterTweet object, or None if tweet not found.
        The tweet may be not found because the Nitter instance runs on a region where the tweet is blocked.
        The 'search_all_instances' parameter can be set to True for searching the tweet in all the configured instances
        until found in one."""
        nitter_instances = self.nitter_instances_unique if search_all_instances else [None]
        endpoint = f"/_/status/{tweet_id}"

        for nitter_instance in nitter_instances:
            html = self._request_nitter(
                endpoint=endpoint,
                nitter_instance=nitter_instance,
                ignore_statuscodes=[404],
            )

            tweet = NitterParser(
                parser=self.beautifulsoup_parser,
                html=html,
            ).get_tweet_from_tweetpage()

            if tweet:
                return tweet
