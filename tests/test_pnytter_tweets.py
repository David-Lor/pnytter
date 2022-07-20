import pytest

from ._test_pnytter_tweets_data import GetTweetsYearprogress


@pytest.mark.parametrize("username, filter_from, filter_to, expected_pages, expected_tweets", [
    pytest.param(
        GetTweetsYearprogress.username,
        GetTweetsYearprogress.filter_from,
        GetTweetsYearprogress.filter_to,
        GetTweetsYearprogress.expected_pages,
        GetTweetsYearprogress.expected_result,
        id=f"@{GetTweetsYearprogress.username}"
    )
])
def test_get_tweets(pnytter, username, filter_from, filter_to, expected_pages, expected_tweets):
    args = (
        username,
        filter_from,
        filter_to,
    )
    generator = pnytter.get_user_tweets(*args)

    pages_results = list()
    tweets_results = list()
    # noinspection PyTypeChecker
    for _ in range(expected_pages + 2):
        try:
            page_results = next(generator)
            assert len(page_results) > 0
        except StopIteration:
            break

        pages_results.append(page_results)
        tweets_results.extend(page_results)

    assert len(pages_results) == expected_pages
    assert tweets_results == expected_tweets

    tweets_results = pnytter.get_user_tweets_list(*args)
    assert tweets_results == expected_tweets
