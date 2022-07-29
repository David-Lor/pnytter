import urllib.parse
import datetime
from typing import List, Tuple, Optional

from bs4.element import Tag

from .base import BaseNitterParser
from ..models import TwitterTweet
from ..utils import Utils


class NitterTweetsParser(BaseNitterParser):

    def get_tweet_from_tweetpage(self) -> Optional[TwitterTweet]:
        if self._get_error() == "Tweet not found":
            return None

        div_maintweet = self.soup.find("div", class_="main-tweet")
        if SearchpageTweetbodyParser.get_unavailable_reason(div_maintweet):
            # TODO Differenciate between tweet not found and unavailable? Current versions of Nitter always return "Unavailable" and not false NotFounds?
            return None

        div_maintweet_tweetbody = div_maintweet.find("div", class_="tweet-body")

        return SearchpageTweetbodyParser(div_maintweet_tweetbody).get_tweet()

    def get_tweets_from_searchpage(self) -> List[TwitterTweet]:
        tweets_divs = self.soup.find_all("div", class_="tweet-body")
        return [self._parse_tweet_from_searchpage_div(div) for div in tweets_divs]

    def get_searchpage_next_cursor(self) -> Optional[str]:
        div = self.soup.find("div", class_="show-more")
        href = div.find("a").get("href")
        # href example: ?f=tweets&cursor=scroll%3AthGAVUV0VFVBaCgLOdg_bM_yoWgoC9ufb4poErEnEV8IV6FYCJehgHREVGQVVMVDUBFQAVAAA%3D

        params_cursor = urllib.parse.parse_qs(href).get("cursor")
        if params_cursor:
            return params_cursor[0]

    def get_searchpage_nextpage_params(self) -> Optional[str]:
        divs = self.soup.find_all("div", class_="show-more")
        try:
            div = next(div for div in divs if div.text == "Load more")
        except StopIteration:
            return None

        return div.find("a").get("href")

    @staticmethod
    def _parse_tweet_from_searchpage_div(tweetbody_div: Tag) -> TwitterTweet:
        return SearchpageTweetbodyParser(tweetbody_div).get_tweet()


class SearchpageTweetbodyParser:
    def __init__(self, tweetbody_div: Tag):
        self.soup = tweetbody_div

    def get_tweet(self) -> TwitterTweet:
        author = self._get_author()
        tweetid, creationdate = self._get_tweetid_creationdate()
        text = self._get_text()
        stats = self._get_stats()

        # noinspection PyTypeChecker
        return TwitterTweet(
            tweet_id=tweetid,
            author=author,
            created_on=creationdate,
            text=text,
            stats=stats,
        )

    def _get_author(self) -> str:
        username = self.soup.find("a", class_="username").text
        return Utils.clean_username(username)

    def _get_tweetid_creationdate(self) -> Tuple[str, datetime.datetime]:
        a = self.soup.find("span", class_="tweet-date").find("a")
        href = a.get("href")  # example: /elonmusk/status/1549605387158134785#m
        title = a.get("title")  # example: Jul 20, 2022 · 4:01 AM UTC

        tweetid = href.split("/")[-1].split("#")[0]

        creationdate_format = "%b %d, %Y · %I:%M %p UTC"
        creationdate = datetime.datetime.strptime(title, creationdate_format).replace(tzinfo=datetime.timezone.utc)

        return tweetid, creationdate

    def _get_text(self) -> str:
        return self.soup.find("div", class_="tweet-content").text

    def _get_stats(self) -> TwitterTweet.Stats:
        div = self.soup.find("div", class_="tweet-stats")
        """This div contains one "icon-container" span per stat.
        Each "icon-container" span contains a span "icon-*" for the icon, identifying the metric shown.
        The metric value is contained on a div, at "icon-container" level.
        For getting each metric, we have to iterate each "icon-container", identifying its "icon-*".
        
        HTML example of the "tweet-stats" div:
        
        <div class="tweet-stats">
            <span class="tweet-stat"><div class="icon-container"><span class="icon-comment" title=""></span> 40</div></span>
            <span class="tweet-stat"><div class="icon-container"><span class="icon-retweet" title=""></span> 1,216</div></span>
            <span class="tweet-stat"><div class="icon-container"><span class="icon-quote" title=""></span> 115</div></span>
            <span class="tweet-stat"><div class="icon-container"><span class="icon-heart" title=""></span> 8,141</div></span>
        </div>
        """

        data_spanclasses = dict(
            # Keys must be same names as attributes from TwitterTweet.Stats.
            # Values are the class of icon spans found within "tweet-stat" spans.
            comments="icon-comment",
            retweets="icon-retweet",
            quotes="icon-quote",
            likes="icon-heart",
        )
        data_values = {k: '' for k in data_spanclasses.keys()}

        for span in div.find_all("span", class_="tweet-stat"):
            for metric_key, metric_span_class in data_spanclasses.items():
                if not span.find("span", class_=metric_span_class):
                    continue
                data_values[metric_key] = span.find("div", class_="icon-container").text

        # noinspection PyTypeChecker
        return TwitterTweet.Stats(**data_values)

    @staticmethod
    def get_unavailable_reason(div_maintweet) -> Optional[str]:
        div = div_maintweet.find("div", class_="unavailable-box")
        if div:
            return div.text
