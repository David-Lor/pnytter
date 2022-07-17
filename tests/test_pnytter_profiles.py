import pytest

from pnytter import TwitterProfile


@pytest.mark.parametrize("username, expected_result", [
    pytest.param(
        "jack",
        TwitterProfile(
            id=12,
            username="jack",
            fullname="jack",
        ),
        id="@jack",
    ),
    pytest.param(
        "elonmusk",
        TwitterProfile(
            id=44196397,
            username="elonmusk",
            fullname="Elon Musk",
        ),
        id="@elonmusk",
    )
])
def test_find_user(pnytter, username, expected_result):
    result = pnytter.find_user(username)
    assert result == expected_result
