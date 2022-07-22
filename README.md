# pnytter

A Python library for scraping Twitter using one or more [Nitter](https://github.com/zedeus/nitter) instances.

## About Nitter & Pnytter

From [Nitter's GitHub repository](https://github.com/zedeus/nitter) description: "A free and open source alternative Twitter front-end focused on privacy and performance".

Pnytter is a Python library that performs requests to Nitter instances for fetching different data from Twitter, requiring no official API credentials, and theorically no rate limits.

## Features

This project currently features the following:

- Supported methods:
  - Get Twitter profile data, by username
  - Get all the Tweets from a profile, by username in a date range
  - Get a single Tweet data by Tweet ID
- Technical details:
  - Usage of multiple Nitter instances (chosen randomly for each request)
  - Return data as [Pydantic](https://pydantic-docs.helpmanual.io) models

The features are bound to the development of my [twitterscraper](https://github.com/David-Lor/twitterscraper). Features may be requested through Issues or (preferably) Pull-Requests.

## Requirements

- Python >= 3.6
- Requirements listed on [requirements.txt](requirements.txt)
- A hosted Nitter instance is recommeded for intensive use, to avoid overloading the public instances

## Installing

Package support is pending.

## Usage

```python
from pnytter import Pnytter
import pprint

pnytter = Pnytter(
  nitter_instances=["https://nitter.net", "https://nitter.pussthecat.org"]
)

# Find the data from a single user
user = pnytter.find_user("jack")
pprint.pp(user.dict())
# {'id': 12,
#  'username': 'jack',
#  'fullname': 'jack',
#  'biography': '#bitcoin',
#  'verified': True,
#  'joined_datetime': datetime.datetime(2006, 3, 21, 20, 50, tzinfo=datetime.timezone.utc),
#  'stats': {'tweets': 28602,
#            'following': 4573,
#            'followers': 6419102,
#            'likes': 35210},
#  'pictures': {'profile': {'twitter_url': HttpUrl('https://pbs.twimg.com/profile_images/1115644092329758721/AFjOr-K8.jpg', scheme='https', host='pbs.twimg.com', tld='com', host_type='domain', port='443', path='/profile_images/1115644092329758721/AFjOr-K8.jpg'),
#                           'nitter_path': '/pic/pbs.twimg.com%2Fprofile_images%2F1115644092329758721%2FAFjOr-K8.jpg'},
#               'banner': {'twitter_url': HttpUrl('https://pbs.twimg.com/profile_banners/12/1584998840/1500x500', scheme='https', host='pbs.twimg.com', tld='com', host_type='domain', port='443', path='/profile_banners/12/1584998840/1500x500'),
#                          'nitter_path': '/pic/https%3A%2F%2Fpbs.twimg.com%2Fprofile_banners%2F12%2F1584998840%2F1500x500'}}}


# Find user tweets during a date range
tweets = pnytter.get_user_tweets_list("year_progress", filter_from="2022-06-01", filter_to="2022-06-25")
pprint.pp(tweets)
# [TwitterTweet(tweet_id=1539246778041745409, author='year_progress', created_on=datetime.datetime(2022, 6, 21, 14, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 47%'),
#  TwitterTweet(tweet_id=1537918020118491136, author='year_progress', created_on=datetime.datetime(2022, 6, 17, 22, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 46%'),
#  TwitterTweet(tweet_id=1536589258370297856, author='year_progress', created_on=datetime.datetime(2022, 6, 14, 6, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 45%'),
#  TwitterTweet(tweet_id=1535275600482816000, author='year_progress', created_on=datetime.datetime(2022, 6, 10, 15, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 44%'),
#  TwitterTweet(tweet_id=1533946844497199104, author='year_progress', created_on=datetime.datetime(2022, 6, 6, 23, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 43%'),
#  TwitterTweet(tweet_id=1532633192020205570, author='year_progress', created_on=datetime.datetime(2022, 6, 3, 8, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 42%')]


# Find single tweet
tweet = pnytter.get_tweet(1539246778041745409)
pprint.pp(tweet.dict())
# {'tweet_id': 1539246778041745409,
#  'author': 'year_progress',
#  'created_on': datetime.datetime(2022, 6, 21, 14, 0, tzinfo=datetime.timezone.utc),
#  'text': '▓▓▓▓▓▓▓░░░░░░░░ 47%'}
```

## Known issues

### Unfixable

- Certain tweets are not available on certain regions due to legal reasons. Pnytter method `get_tweet` allows forcing the query of all available Nitter instances until available in one of them.

### Solvable (pending)

- The URL parsing of media (profile pictures) does not work with certain instances (known: `nitter.domain.glass`), in which case the object initialization fails.

## Changelog

Versions 0.y.z are expected to be unstable, and the API may change on Minor (y) releases.

- 0.0.1
  - Initial release:
    - Get profile by username: id, username, fullname, biography, verified, when joined, stats (count of tweets, following, followers, likes), pictures (profile, banner)
    - Get profile tweets in date range (tweet id, author, when posted, text)
    - Get single tweet
