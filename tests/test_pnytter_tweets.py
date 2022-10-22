from typing import List

import pytest

from pnytter import TwitterTweet

from tests._test_pnytter_tweets_data import BaseGetTweetsScenario, GetTweetsYearprogress, NonExistingTweetId, GermanyBlockedTweet


# TODO Ignoring failures on this test, because of bug on Nitter causing search randomly missing tweets.
#      Remove the pytest.mark.flaky when this gets fixed.
@pytest.mark.flaky
@pytest.mark.parametrize("scenario", [
    pytest.param(
        GetTweetsYearprogress,
        id=f"@{GetTweetsYearprogress.username}",
    )
])
def test_get_tweets(pnytter, scenario: BaseGetTweetsScenario):
    args = (
        scenario.username,
        scenario.filter_from,
        scenario.filter_to,
    )
    expected_pages = scenario.get_expected_pages()
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
    _assert_tweets(
        actual=tweets_results,
        expected=scenario.expected_tweets,
        assert_stats=True,
    )

    # Compare result obtained from get_user_tweets_list() with result obtained from get_user_tweets() generator
    user_tweets_results = pnytter.get_user_tweets_list(*args)
    assert user_tweets_results == tweets_results


@pytest.mark.parametrize("tweet_id, expected_tweet", [
    pytest.param(
        None,
        GetTweetsYearprogress.expected_tweets[0],
        id=str(GetTweetsYearprogress.expected_tweets[0].tweet_id),
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


def _assert_tweets(actual: List[TwitterTweet], expected: List[TwitterTweet], assert_as_is: bool = False, assert_stats: bool = False):
    actual_map = {tweet.tweet_id: tweet for tweet in actual}
    expected_map = {tweet.tweet_id: tweet for tweet in expected}
    assert sorted(list(actual_map.keys())) == sorted(list(expected_map.keys()))

    for tweet_id, actual in actual_map.items():
        expected = expected_map[tweet_id]
        _assert_tweet(
            actual=actual,
            expected=expected,
            assert_as_is=assert_as_is,
            assert_stats=assert_stats,
        )


def _assert_tweet(actual: TwitterTweet, expected: TwitterTweet, assert_as_is: bool = False, assert_stats: bool = False):
    if assert_as_is or (expected is None or actual is None):
        assert actual == expected
        return

    excludes = {"stats"}
    assert expected.dict(exclude=excludes) == actual.dict(exclude=excludes)
    if assert_stats:
        _assert_tweet_stats(actual.stats, expected.stats)


def _assert_tweet_stats(actual: TwitterTweet.Stats, expected: TwitterTweet.Stats):
    actual_dict = actual.dict()
    for k, expected_value in expected.dict().items():
        actual_value = actual_dict[k]
        assert pytest.approx(actual_value, rel=100) == expected_value
