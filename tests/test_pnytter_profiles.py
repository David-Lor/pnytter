import uuid

import pytest
import pydantic

from pnytter import TwitterProfile, TwitterURL


class ProfileTestParams(pydantic.BaseModel):
    username: str
    assert_biography: bool = True
    assert_pictures: bool = True


# noinspection PyTypeChecker
@pytest.mark.parametrize("profile_test_params, expected_result", [
    pytest.param(
        ProfileTestParams(
            username="possumeveryhour",
        ),
        TwitterProfile(
            id=1022089486849765376,
            username="PossumEveryHour",
            fullname="Possumeveryhour.io",
            biography="All images belong to their original owners. See possumeveryhour.io for more places other than Twitter where to find your poss fix.",
            verified=False,
            joined_datetime="2018-07-25T12:01:00Z",
            stats=TwitterProfile.Stats(
                # at 2023-06-24, decreased to less than expected
                tweets=34100,
                following=1,
                followers=560000,
                likes=0,
            ),
            pictures=TwitterProfile.Pictures(
                profile=TwitterURL(
                    nitter_path="/pic/pbs.twimg.com%2Fprofile_images%2F1022090933343608833%2FxZvdXf7E.jpg",
                    twitter_url="https://pbs.twimg.com/profile_images/1022090933343608833/xZvdXf7E.jpg",
                ),
                banner=TwitterURL(
                    nitter_path="/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F1022089486849765376%2F1546021838%2F1500x500",
                    twitter_url="https://pbs.twimg.com/profile_banners/1022089486849765376/1546021838/1500x500",
                ),
            ),
        ),
        id="@PossumEveryHour",
    ),
    pytest.param(
        ProfileTestParams(
            username="nobio",
            assert_pictures=False,
        ),
        TwitterProfile(
            id=None,
            username="nobio",
            fullname="Gernot",
            biography="",
            verified=False,
            joined_datetime="2008-05-17T21:30:00Z",
            stats=TwitterProfile.Stats(
                # at 2022-10-17, decreased
                tweets=17,
                following=78,
                followers=7,
                likes=27,
            ),
            pictures=TwitterProfile.Pictures(),
        ),
        id="@nobio",
    ),
    pytest.param(
        ProfileTestParams(
            username=str(uuid.uuid4()),
        ),
        None,
        id="non existing",
    ),
])
def test_find_user(pnytter, profile_test_params: ProfileTestParams, expected_result: TwitterProfile):
    result = pnytter.find_user(profile_test_params.username)
    if expected_result is None:
        assert result is None
        return

    exclude_fields = {"stats"}
    if not profile_test_params.assert_biography:
        exclude_fields.add("biography")
    if not profile_test_params.assert_pictures:
        exclude_fields.add("pictures")

    result_data = result.dict(exclude=exclude_fields)
    expected_data = expected_result.dict(exclude=exclude_fields)
    assert result_data == expected_data

    result_stats_data = result.stats.dict()
    for stat_key, stat_expected_value in expected_result.stats.dict().items():
        stat_result_value = result_stats_data[stat_key]
        assert stat_result_value >= stat_expected_value, stat_key
