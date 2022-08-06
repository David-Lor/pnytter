import random
import datetime
from typing import List, Collection, Optional, Union, Generator

import pydantic
import requests
from urljoin import url_path_join

from .nitter_parser import NitterParser
from .models import TwitterProfile, TwitterTweet
from .exceptions import NoNitterInstancesDefinedError
from .utils import Utils

__all__ = ("Pnytter",)


class Pnytter(pydantic.BaseModel):
    """Main Pnytter class, with all the Pnytter features as public methods.
    """

    nitter_instances: Union[List[pydantic.AnyHttpUrl], pydantic.AnyHttpUrl] = []
    """List of the Nitter instances to use. Each instance must be given as the base URL of the Nitter server.
    At least one instance is required, in which case can be given plain (without a list).

    The Pnytter class can be initialized providing no `nitter_instances`. However, the NoNitterInstancesDefinedError
    will be raised when calling a class method that requires requesting Nitter, if no instances are set.
    The `add_instance` method can be used for adding instances after initializing the Pnytter class.

    Instances may be repeated for increasing their chances;
    when all the instances must be used (like in `get_tweet` with `search_all_instances=True`)
    the repeated elements are ignored for querying.
    """

    beautifulsoup_parser: str = "html.parser"
    """BeautifulSoup parser to use for parsing Nitter's HTML.
    """

    request_timeout: float = pydantic.Field(default=10, ge=0)
    """Timeout in seconds (allowing decimals) for HTTP requests (default: 10, allows decimals).
    """

    class Config(pydantic.BaseConfig):
        validate_assignment = True

    @pydantic.validator("nitter_instances")
    def _nitter_instances_single_to_list(cls, v):
        """If the 'nitter_instances' attribute is not a list, set it as a list with itself as single value.
        """
        if not isinstance(v, list):
            v = [v]
        return v

    @property
    def nitter_instances_unique(self):
        """Return a set of the 'nitter_instances' configured, for ignoring duplicates.
        """
        return set(str(instance) for instance in self.nitter_instances)

    def _get_random_nitter_instance(self) -> str:
        """Retrieve a random Nitter instance URL from the 'nitter_instances' list.
        """
        return random.choice(self.nitter_instances)

    def _validate_instances_available(self):
        if not self.nitter_instances:
            raise NoNitterInstancesDefinedError

    def _raw_request(
            self,
            method: str,
            url: str,
            params: Optional[dict],
            ignore_statuscodes: Collection[int]
    ) -> str:
        """Method for performing an HTTP request, and returning the response body as string.
        This method can be overriden by the code that uses Pnytter, if required.
        """
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
        This method chooses a random Nitter instance to use for the request, unless one specifically given.
        """
        self._validate_instances_available()
        nitter_instance = nitter_instance if nitter_instance else self._get_random_nitter_instance()
        url = url_path_join(nitter_instance, endpoint)

        return self._raw_request(
            method=method,
            url=url,
            params=params,
            ignore_statuscodes=ignore_statuscodes or (),
        )

    def add_instance(self, instance_url: str, times: int = 1):
        """Add a Nitter instance for usage.

        :param instance_url: Nitter instance URL.
        :param times: how many times to repeat the instance (default: 1).
        """
        for _ in range(times):
            # noinspection PyTypeChecker
            self.nitter_instances.append(instance_url)

    def find_user(
            self,
            username: str
    ) -> Optional[TwitterProfile]:
        """Get the information of a Twitter user, given its public username. If the profile does not exist, return None.

        :param username: Twitter profile username (example: "@jack").
        :return: TwitterProfile if found; None if not found.
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
    ) -> Generator[List[TwitterTweet], None, None]:
        """Get all the tweets from a username. Basic retweets (RTs without a custom comment) will not be returned.
        The found tweets are yield as a generator, for each page of results fetched from Nitter.
        The method 'get_user_tweets_list' may be used for the same functionality, but returning the results at once.

        :param username: username of the profile to search tweets from.
        :param filter_from: filter from a date (inclusive). Given as datetime.date or a string with format 'YYYY-MM-DD'.
        :param filter_to: filter until a date (exclusive). Given as datetime.date or a string with format 'YYYY-MM-DD'.
        :return: Generator that returns lists of TwitterTweet objects in batch, for each page of results parsed.
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
        method documentation for more details and the list of arguments supported.
        """
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

        The Tweet may be not found because the Nitter instance runs on a region where the Tweet is blocked;
        the 'search_all_instances' parameter can be set to True for trying lookup in all configured instances.

        :param tweet_id: Tweet ID.
        :param search_all_instances: if True, searching the tweet in all the configured instances until found in one.
        :return: TwitterTweet if found; None if not found or unavailable where used Nitter instance is hosted.
        """
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
