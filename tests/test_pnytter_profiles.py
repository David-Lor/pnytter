import uuid

import pytest

from pnytter import TwitterProfile


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
