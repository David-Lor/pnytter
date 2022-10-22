import fnmatch
import datetime
from typing import Optional

from .base import BaseNitterParser
from ..models import TwitterProfile


class NitterProfilesParser(BaseNitterParser):
    def get_profile(self) -> Optional[TwitterProfile]:
        if self._is_profile_notfound():
            return None

        username = self._get_profile_username()
        fullname = self._get_profile_fullname()
        biography = self._get_profile_biography()
        verified = self._get_profile_verified()
        joined_datetime = self._get_profile_join_datetime()
        stats = self._get_profile_stats()
        # TODO Parse profile_id
        profile_id = None

        # noinspection PyTypeChecker
        return TwitterProfile(
            id=profile_id,
            username=username,
            fullname=fullname,
            biography=biography,
            verified=verified,
            joined_datetime=joined_datetime,
            stats=stats,
        )

    def _is_profile_notfound(self) -> bool:
        errorpanel = self.soup.find("div", class_="error-panel")
        if not errorpanel:
            return False
        return fnmatch.fnmatch(errorpanel.text, """User "*" not found""")

    def _get_profile_username(self) -> str:
        # Remove the first character ("@") from the element
        return self.soup.find("a", class_="profile-card-username").text[1:]

    def _get_profile_fullname(self) -> str:
        return self.soup.find("a", class_="profile-card-fullname").text

    def _get_profile_biography(self) -> str:
        div = self.soup.find("div", class_="profile-bio")
        return div.text if div else ""

    def _get_profile_verified(self) -> bool:
        return self.soup.find("span", class_="verified-icon") is not None

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
            tweets=posts,
            following=following,
            followers=followers,
            likes=likes,
        )
