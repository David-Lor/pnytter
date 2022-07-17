import fnmatch
import datetime
from typing import Optional

import parse
from bs4 import BeautifulSoup

from .models import TwitterProfile


class NitterParser:
    def __init__(self, data: str):
        """
        :param data: Nitter HTML source to parse
        """
        self.data = data
        self.soup = BeautifulSoup(self.data, "html")

    def get_profile(self) -> Optional[TwitterProfile]:
        if self._is_profile_notfound():
            return None

        profile_id = self._get_profile_id()
        username = self._get_profile_username()
        fullname = self._get_profile_fullname()
        biography = self._get_profile_biography()
        joined_datetime = self._get_profile_join_datetime()
        stats = self._get_profile_stats()

        return TwitterProfile(
            id=profile_id,  # noqa
            username=username,
            fullname=fullname,
            biography=biography,
            joined_datetime=joined_datetime,
            stats=stats,
        )

    def _is_profile_notfound(self) -> bool:
        errorpanel = self.soup.find("div", class_="error-panel")
        if not errorpanel:
            return False
        return fnmatch.fnmatch(errorpanel.text, """User "*" not found""")

    def _get_profile_id(self) -> str:
        profile_banner = self.soup.find("div", class_="profile-banner")
        # Given:
        # <div class="profile-banner"><a href="/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500" target="_blank"><img src="/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500" alt="" /></a></div>
        # the userid is 12

        profile_banner_href = profile_banner.find("a").get("href")
        # Given:
        # '/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500'
        # the userid is 12

        profile_banner_href = profile_banner_href.replace("/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F", "")
        # Given:
        # '12%2F1584998840%2F1500x500'
        # the userid is 12 (first characters before '%2F'...)

        return profile_banner_href.split("%2F")[0]

    def _get_profile_username(self) -> str:
        # Remove the first character ("@") from the element
        return self.soup.find("a", class_="profile-card-username").text[1:]

    def _get_profile_fullname(self) -> str:
        return self.soup.find("a", class_="profile-card-fullname").text

    def _get_profile_biography(self) -> str:
        return self.soup.find("div", class_="profile-bio").text

    def _get_profile_join_datetime(self) -> datetime.datetime:
        value = self.soup.find("div", class_="profile-joindate").find("span").get("title")

        # Example: '8:50 PM - 21 Mar 2006'
        datetime_format = "%I:%M %p - %d %b %Y"

        return datetime.datetime.strptime(value, datetime_format).replace(tzinfo=datetime.timezone.utc)

    def _get_profile_stats(self) -> TwitterProfile.Stats:
        ul = self.soup.find("ul", class_="profile-statlist")
        posts = ul.find("li", class_="posts").text
        following = ul.find("li", class_="following").text
        followers = ul.find("li", class_="followers").text
        likes = ul.find("li", class_="likes").text

        return TwitterProfile.Stats(
            tweets=posts,  # noqa
            following=following,  # noqa
            followers=followers,  # noqa
            likes=likes,  # noqa
        )
