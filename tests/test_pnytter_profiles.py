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
    assert result == expected_result
