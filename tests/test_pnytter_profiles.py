import uuid

import pytest

from pnytter import TwitterProfile, TwitterURL


# noinspection PyTypeChecker
@pytest.mark.parametrize("username, expected_result", [
    pytest.param(
        "jack",
        TwitterProfile(
            id=12,
            username="jack",
            fullname="jack",
            biography="#bitcoin",
            joined_datetime="2006-03-21T20:50:00Z",  # noqa
            stats=TwitterProfile.Stats(
                # at 2022-07-17, decreased
                tweets=28000,
                following=4500,
                followers=6419000,
                likes=35000,
            ),
            pictures=TwitterProfile.Pictures(
                profile=TwitterURL(
                    nitter_path="/pic/pbs.twimg.com%2Fprofile_images%2F1115644092329758721%2FAFjOr-K8.jpg",
                    twitter_url="https://pbs.twimg.com/profile_images/1115644092329758721/AFjOr-K8.jpg",
                ),
                banner=TwitterURL(
                    nitter_path="/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500",
                    twitter_url="https://pbs.twimg.com/profile_banners/12/1584998840/1500x500",
                ),
            ),
        ),
        id="@jack",
    ),
    pytest.param(
        "elonmusk",
        TwitterProfile(
            id=44196397,
            username="elonmusk",
            fullname="Elon Musk",
            biography="Mars & Cars, Chips & Dips",
            joined_datetime="2009-06-02T20:12:00Z",  # noqa
            stats=TwitterProfile.Stats(
                # at 2022-07-17, decreased
                tweets=18700,
                following=110,
                followers=101465000,
                likes=13500,
            ),
            pictures=TwitterProfile.Pictures(
                profile=TwitterURL(
                    nitter_path="/pic/pbs.twimg.com%2Fprofile_images%2F1529956155937759233%2FNyn1HZWF.jpg",
                    twitter_url="https://pbs.twimg.com/profile_images/1529956155937759233/Nyn1HZWF.jpg",
                ),
                banner=TwitterURL(
                    nitter_path="/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F44196397%2F1576183471%2F1500x500",
                    twitter_url="https://pbs.twimg.com/profile_banners/44196397/1576183471/1500x500",
                ),
            ),
        ),
        id="@elonmusk",
    ),
    pytest.param(
        str(uuid.uuid4()),
        None,
        id="non existing",
    ),
])
def test_find_user(pnytter, username, expected_result):
    result = pnytter.find_user(username)
    if expected_result is None:
        assert result is None
        return

    exclude_fields = {"stats"}
    result_data = result.dict(exclude=exclude_fields)
    expected_data = expected_result.dict(exclude=exclude_fields)
    assert result_data == expected_data

    result_stats_data = result.stats.dict()
    for stat_key, stat_expected_value in expected_result.stats.dict().items():
        stat_result_value = result_stats_data[stat_key]
        assert stat_result_value >= stat_expected_value, stat_key
