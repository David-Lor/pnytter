import uuid

import pytest
import pydantic

from pnytter import TwitterProfile


class ProfileTestParams(pydantic.BaseModel):
    username: str
    assert_biography: bool = True


# TODO Ignoring failures on this test because of failing profile pictures parsing.
#      Remove the pytest.mark.flaky when #7 gets fixed
# noinspection PyTypeChecker
@pytest.mark.flaky
@pytest.mark.parametrize("profile_test_params, expected_result", [
    pytest.param(
        ProfileTestParams(
            username="jack",
        ),
        TwitterProfile(
            id=12,
            username="jack",
            fullname="jack",
            biography="#bitcoin",
            verified=True,
            joined_datetime="2006-03-21T20:50:00Z",
            stats=TwitterProfile.Stats(
                # at 2022-07-17, decreased
                tweets=28000,
                following=4500,
                followers=6410000,
                likes=35000,
            ),
        ),
        id="@jack",
    ),
    pytest.param(
        ProfileTestParams(
            username="elonmusk",
            assert_biography=False,
        ),
        TwitterProfile(
            id=44196397,
            username="elonmusk",
            fullname="Elon Musk",
            biography="Mars & Cars, Chips & Dips",
            verified=True,
            joined_datetime="2009-06-02T20:12:00Z",
            stats=TwitterProfile.Stats(
                # at 2022-07-17, decreased
                tweets=18700,
                following=110,
                followers=101465000,
                likes=13500,
            ),
        ),
        id="@elonmusk",
    ),
    pytest.param(
        ProfileTestParams(
            username="possumeveryhour",
        ),
        TwitterProfile(
            id=1022089486849765376,
            username="PossumEveryHour",
            fullname="Possum Every Hour",
            biography="All images belong to their original owners. Failures may occassionally occur. For problems and new image submissions DM @ThunderySteak",
            verified=False,
            joined_datetime="2018-07-25T12:01:00Z",
            stats=TwitterProfile.Stats(
                # at 2022-07-18, decreased
                tweets=34100,
                following=1,
                followers=571300,
                likes=0,
            ),
        ),
        id="@PossumEveryHour",
    ),
    pytest.param(
        ProfileTestParams(
            username="nobio",
        ),
        TwitterProfile(
            id=14814846,
            username="nobio",
            fullname="Gernot",
            biography="",
            verified=False,
            joined_datetime="2008-05-25T12:01:00Z",
            stats=TwitterProfile.Stats(
                # at 2022-10-17, decreased
                tweets=17,
                following=78,
                followers=7,
                likes=27,
            ),
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

    result_data = result.dict(exclude=exclude_fields)
    expected_data = expected_result.dict(exclude=exclude_fields)
    assert result_data == expected_data

    result_stats_data = result.stats.dict()
    for stat_key, stat_expected_value in expected_result.stats.dict().items():
        stat_result_value = result_stats_data[stat_key]
        assert stat_result_value >= stat_expected_value, stat_key
