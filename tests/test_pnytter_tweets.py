import pytest

from pnytter import TwitterTweet

from tests._test_pnytter_tweets_data import GetTweetsYearprogress, NonExistingTweetId, GermanyBlockedTweet


@pytest.mark.parametrize("username, filter_from, filter_to, expected_pages, expected_tweets", [
    pytest.param(
        GetTweetsYearprogress.username,
        GetTweetsYearprogress.filter_from,
        GetTweetsYearprogress.filter_to,
        GetTweetsYearprogress.expected_pages,
        GetTweetsYearprogress.expected_result,
        id=f"@{GetTweetsYearprogress.username}",
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
    for i, tweet_result in enumerate(tweets_results):
        expected_tweet = expected_tweets[i]
        _assert_tweet(expected=expected_tweet, actual=tweet_result, assert_stats=True)

    user_tweets_results = pnytter.get_user_tweets_list(*args)
    assert user_tweets_results == tweets_results


@pytest.mark.parametrize("tweet_id, expected_tweet", [
    pytest.param(
        None,
        GetTweetsYearprogress.expected_result[0],
        id=str(GetTweetsYearprogress.expected_result[0].tweet_id),
    ),
    pytest.param(
        NonExistingTweetId,
        None,
        id="nonexisting tweetid"
    )
])
def test_get_single_tweet(pnytter, tweet_id: str, expected_tweet: TwitterTweet):
    if not tweet_id and expected_tweet:
        tweet_id = expected_tweet.tweet_id

    result = pnytter.get_tweet(tweet_id, search_all_instances=True)
    _assert_tweet(expected=expected_tweet, actual=result, assert_stats=True)


def test_get_unavailable_tweet_single_instance(pnytter):
    """Get a tweet blocked in Germany, from a public Nitter instance hosted on Germany.
    The tweet should not be returned."""
    pnytter.nitter_instances = ["https://nitter.pussthecat.org"]

    result = pnytter.get_tweet(GermanyBlockedTweet.tweet_id)
    assert result is None


def test_get_unavailable_tweet_multiple_instances(pnytter):
    """Get a tweet blocked in Germany, using public instances hosted on Germany and other countries.
    The tweet should eventually be returned."""
    pnytter.nitter_instances = [
        # German instances
        "https://nitter.pussthecat.org",
        "https://nitter.grimneko.de",
        # Other instances
        "https://nitter.ca",
    ]

    # TODO Capture requests performed and assert the instances requested

    result = pnytter.get_tweet(GermanyBlockedTweet.tweet_id, search_all_instances=True)
    _assert_tweet(actual=result, expected=GermanyBlockedTweet)


def _assert_tweet(actual: TwitterTweet, expected: TwitterTweet, assert_as_is: bool = False, assert_stats: bool = False):
    if assert_as_is or (expected is None or actual is None):
        assert actual == expected
        return

    assert expected.dict(exclude={"stats"}) == actual.dict(exclude={"stats"})
    if assert_stats:
        _assert_tweet_stats(actual.stats, expected.stats)


def _assert_tweet_stats(actual: TwitterTweet.Stats, expected: TwitterTweet.Stats):
    actual_dict = actual.dict()
    for k, expected_value in expected.dict().items():
        actual_value = actual_dict[k]
        assert pytest.approx(actual_value, rel=100) == expected_value
