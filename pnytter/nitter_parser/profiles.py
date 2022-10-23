import fnmatch
import datetime
from typing import Optional

from .base import BaseNitterParser
from ..models import TwitterProfile, TwitterURL


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
        pictures = self._get_profile_pictures()
        profile_id = self._get_profile_id_from_profile_pictures(pictures)

        # noinspection PyTypeChecker
        return TwitterProfile(
            id=profile_id,
            username=username,
            fullname=fullname,
            biography=biography,
            verified=verified,
            joined_datetime=joined_datetime,
            stats=stats,
            pictures=pictures,
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
        # TODO Returning True if the user is not verified but retweeted from a verified account?
        #  (must search the span inside its header)
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

    def _get_profile_pictures(self) -> TwitterProfile.Pictures:
        # TODO Failing for certain instances (nitter.domain.glass)
        pic_profile_src, pic_banner_src = None, None

        pic_profile_a = self.soup.find("a", class_="profile-card-avatar")
        if pic_profile_a:
            pic_profile_src = pic_profile_a.get("href")

        pic_banner_div = self.soup.find("div", class_="profile-banner")
        if pic_banner_div:
            pic_banner_a = pic_banner_div.find("a")
            if pic_banner_a:
                pic_banner_src = pic_banner_a.get("href")

        pic_profile, pic_banner = None, None
        if pic_profile_src and "default_profile" not in pic_profile_src:
            pic_profile = TwitterURL.from_nitter_path(pic_profile_src)
        if pic_banner_src:
            pic_banner = TwitterURL.from_nitter_path(pic_banner_src)

        return TwitterProfile.Pictures(
            profile=pic_profile,
            banner=pic_banner,
        )

    @staticmethod
    def _get_profile_id_from_profile_pictures(pictures: TwitterProfile.Pictures) -> Optional[str]:
        if not pictures.banner:
            return None

        banner_path = pictures.banner.twitter_url.path
        # if banner_path="/profile_banners/12/1584998840/1500x500"
        # then profile_id="12"

        banner_path_chunks = banner_path.split("/")
        chunk_index = banner_path_chunks.index("profile_banners") + 1
        return banner_path_chunks[chunk_index]
