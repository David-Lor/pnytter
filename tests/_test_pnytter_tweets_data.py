import datetime
import math
import base64

from pnytter import TwitterTweet
from pnytter.utils import Const


class GetTweetsYearprogress:
    username = "year_progress"
    filter_from = "2022-01-04"
    filter_to = "2022-06-28"
    expected_result = [TwitterTweet(tweet_id=1540560429335908353, author='year_progress', created_on=datetime.datetime(2022, 6, 25, 5, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 48%', stats=TwitterTweet.Stats(comments=40, retweets=1216, quotes=115, likes=8141)),
                       TwitterTweet(tweet_id=1539246778041745409, author='year_progress', created_on=datetime.datetime(2022, 6, 21, 14, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 47%', stats=TwitterTweet.Stats(comments=29, retweets=1066, quotes=113, likes=5497)),
                       TwitterTweet(tweet_id=1537918020118491136, author='year_progress', created_on=datetime.datetime(2022, 6, 17, 22, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 46%', stats=TwitterTweet.Stats(comments=26, retweets=984, quotes=102, likes=5866)),
                       TwitterTweet(tweet_id=1536589258370297856, author='year_progress', created_on=datetime.datetime(2022, 6, 14, 6, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 45%', stats=TwitterTweet.Stats(comments=40, retweets=1490, quotes=144, likes=7543)),
                       TwitterTweet(tweet_id=1535275600482816000, author='year_progress', created_on=datetime.datetime(2022, 6, 10, 15, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓▓░░░░░░░░ 44%', stats=TwitterTweet.Stats(comments=21, retweets=937, quotes=95, likes=5879)),
                       TwitterTweet(tweet_id=1533946844497199104, author='year_progress', created_on=datetime.datetime(2022, 6, 6, 23, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 43%', stats=TwitterTweet.Stats(comments=42, retweets=1090, quotes=121, likes=7327)),
                       TwitterTweet(tweet_id=1532633192020205570, author='year_progress', created_on=datetime.datetime(2022, 6, 3, 8, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 42%', stats=TwitterTweet.Stats(comments=31, retweets=1152, quotes=165, likes=7021)),
                       TwitterTweet(tweet_id=1531304440162033669, author='year_progress', created_on=datetime.datetime(2022, 5, 30, 16, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 41%', stats=TwitterTweet.Stats(comments=29, retweets=1131, quotes=165, likes=6405)),
                       TwitterTweet(tweet_id=1529975694427668481, author='year_progress', created_on=datetime.datetime(2022, 5, 27, 0, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 40%', stats=TwitterTweet.Stats(comments=39, retweets=1944, quotes=325, likes=9212)),
                       TwitterTweet(tweet_id=1528662030105956355, author='year_progress', created_on=datetime.datetime(2022, 5, 23, 9, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 39%', stats=TwitterTweet.Stats(comments=30, retweets=1118, quotes=116, likes=7013)),
                       TwitterTweet(tweet_id=1527333269263425537, author='year_progress', created_on=datetime.datetime(2022, 5, 19, 17, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 38%', stats=TwitterTweet.Stats(comments=17, retweets=1001, quotes=84, likes=6033)),
                       TwitterTweet(tweet_id=1526019612739092482, author='year_progress', created_on=datetime.datetime(2022, 5, 16, 2, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓▓░░░░░░░░░ 37%', stats=TwitterTweet.Stats(comments=34, retweets=1190, quotes=93, likes=7843)),
                       TwitterTweet(tweet_id=1524690867876945920, author='year_progress', created_on=datetime.datetime(2022, 5, 12, 10, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 36%', stats=TwitterTweet.Stats(comments=19, retweets=1009, quotes=77, likes=6559)),
                       TwitterTweet(tweet_id=1523362102827962370, author='year_progress', created_on=datetime.datetime(2022, 5, 8, 18, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 35%', stats=TwitterTweet.Stats(comments=32, retweets=1231, quotes=87, likes=6781)),
                       TwitterTweet(tweet_id=1522048455669133313, author='year_progress', created_on=datetime.datetime(2022, 5, 5, 3, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 34%', stats=TwitterTweet.Stats(comments=26, retweets=1062, quotes=86, likes=6446)),
                       TwitterTweet(tweet_id=1520719702296829953, author='year_progress', created_on=datetime.datetime(2022, 5, 1, 11, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 33%', stats=TwitterTweet.Stats(comments=48, retweets=1855, quotes=313, likes=9725)),
                       TwitterTweet(tweet_id=1519406038415462400, author='year_progress', created_on=datetime.datetime(2022, 4, 27, 20, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 32%', stats=TwitterTweet.Stats(comments=22, retweets=949, quotes=74, likes=5912)),
                       TwitterTweet(tweet_id=1518077277489270785, author='year_progress', created_on=datetime.datetime(2022, 4, 24, 4, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 31%', stats=TwitterTweet.Stats(comments=31, retweets=1196, quotes=115, likes=7971)),
                       TwitterTweet(tweet_id=1516748523458514956, author='year_progress', created_on=datetime.datetime(2022, 4, 20, 12, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓▓░░░░░░░░░░ 30%', stats=TwitterTweet.Stats(comments=44, retweets=1990, quotes=271, likes=8701)),
                       TwitterTweet(tweet_id=1515434872327843841, author='year_progress', created_on=datetime.datetime(2022, 4, 16, 21, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 29%', stats=TwitterTweet.Stats(comments=41, retweets=1081, quotes=63, likes=7084)),
                       TwitterTweet(tweet_id=1514106119383359496, author='year_progress', created_on=datetime.datetime(2022, 4, 13, 5, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 28%', stats=TwitterTweet.Stats(comments=23, retweets=1096, quotes=75, likes=6698)),
                       TwitterTweet(tweet_id=1512792456886362113, author='year_progress', created_on=datetime.datetime(2022, 4, 9, 14, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 27%', stats=TwitterTweet.Stats(comments=29, retweets=1023, quotes=99, likes=6521)),
                       TwitterTweet(tweet_id=1511463699281756163, author='year_progress', created_on=datetime.datetime(2022, 4, 5, 22, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 26%', stats=TwitterTweet.Stats(comments=29, retweets=1038, quotes=112, likes=6563)),
                       TwitterTweet(tweet_id=1510979561009426438, author='year_progress', created_on=datetime.datetime(2022, 4, 4, 13, 56, tzinfo=datetime.timezone.utc), text="I don't understand. How would you represent 25% with 15 block characters? It's just rounding to the nearest.", stats=TwitterTweet.Stats(comments=1, retweets=0, quotes=0, likes=8)),
                       TwitterTweet(tweet_id=1510134952658182144, author='year_progress', created_on=datetime.datetime(2022, 4, 2, 6, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 25%', stats=TwitterTweet.Stats(comments=84, retweets=3208, quotes=565, likes=13966)),
                       TwitterTweet(tweet_id=1508821297433919491, author='year_progress', created_on=datetime.datetime(2022, 3, 29, 15, 0, tzinfo=datetime.timezone.utc), text='▓▓▓▓░░░░░░░░░░░ 24%', stats=TwitterTweet.Stats(comments=41, retweets=1237, quotes=147, likes=7669)),
                       TwitterTweet(tweet_id=1507492540542562304, author='year_progress', created_on=datetime.datetime(2022, 3, 25, 23, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 23%', stats=TwitterTweet.Stats(comments=24, retweets=997, quotes=75, likes=6462)),
                       TwitterTweet(tweet_id=1506178882566864897, author='year_progress', created_on=datetime.datetime(2022, 3, 22, 8, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 22%', stats=TwitterTweet.Stats(comments=34, retweets=1092, quotes=112, likes=7271)),
                       TwitterTweet(tweet_id=1504865222602985484, author='year_progress', created_on=datetime.datetime(2022, 3, 18, 17, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 21%', stats=TwitterTweet.Stats(comments=46, retweets=1062, quotes=129, likes=6888)),
                       TwitterTweet(tweet_id=1503521366687027202, author='year_progress', created_on=datetime.datetime(2022, 3, 15, 0, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 20%', stats=TwitterTweet.Stats(comments=59, retweets=2493, quotes=456, likes=11515)),
                       TwitterTweet(tweet_id=1502207708023377926, author='year_progress', created_on=datetime.datetime(2022, 3, 11, 9, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 19%', stats=TwitterTweet.Stats(comments=34, retweets=1131, quotes=114, likes=7528)),
                       TwitterTweet(tweet_id=1500878958522511369, author='year_progress', created_on=datetime.datetime(2022, 3, 7, 17, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 18%', stats=TwitterTweet.Stats(comments=37, retweets=1151, quotes=130, likes=7498)),
                       TwitterTweet(tweet_id=1499565304288096257, author='year_progress', created_on=datetime.datetime(2022, 3, 4, 2, 0, tzinfo=datetime.timezone.utc), text='▓▓▓░░░░░░░░░░░░ 17%', stats=TwitterTweet.Stats(comments=24, retweets=1135, quotes=159, likes=7724)),
                       TwitterTweet(tweet_id=1498236551733596160, author='year_progress', created_on=datetime.datetime(2022, 2, 28, 10, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 16%', stats=TwitterTweet.Stats(comments=49, retweets=1231, quotes=149, likes=8739)),
                       TwitterTweet(tweet_id=1496907797790965761, author='year_progress', created_on=datetime.datetime(2022, 2, 24, 18, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 15%', stats=TwitterTweet.Stats(comments=59, retweets=1603, quotes=229, likes=9987)),
                       TwitterTweet(tweet_id=1495594132064116737, author='year_progress', created_on=datetime.datetime(2022, 2, 21, 3, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 14%', stats=TwitterTweet.Stats(comments=43, retweets=1305, quotes=106, likes=8727)),
                       TwitterTweet(tweet_id=1494265376909180929, author='year_progress', created_on=datetime.datetime(2022, 2, 17, 11, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 13%', stats=TwitterTweet.Stats(comments=36, retweets=1190, quotes=107, likes=7663)),
                       TwitterTweet(tweet_id=1492951726080544772, author='year_progress', created_on=datetime.datetime(2022, 2, 13, 20, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 12%', stats=TwitterTweet.Stats(comments=43, retweets=1306, quotes=108, likes=8677)),
                       TwitterTweet(tweet_id=1491622965125038084, author='year_progress', created_on=datetime.datetime(2022, 2, 10, 4, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 11%', stats=TwitterTweet.Stats(comments=36, retweets=1248, quotes=133, likes=8975)),
                       TwitterTweet(tweet_id=1490294212050440204, author='year_progress', created_on=datetime.datetime(2022, 2, 6, 12, 0, tzinfo=datetime.timezone.utc), text='▓▓░░░░░░░░░░░░░ 10%', stats=TwitterTweet.Stats(comments=169, retweets=4001, quotes=818, likes=22556)),
                       TwitterTweet(tweet_id=1488980553554706442, author='year_progress', created_on=datetime.datetime(2022, 2, 2, 21, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 9%', stats=TwitterTweet.Stats(comments=45, retweets=1272, quotes=137, likes=9167)),
                       TwitterTweet(tweet_id=1487651800656367621, author='year_progress', created_on=datetime.datetime(2022, 1, 30, 5, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 8%', stats=TwitterTweet.Stats(comments=39, retweets=1326, quotes=130, likes=9631)),
                       TwitterTweet(tweet_id=1486338145385959429, author='year_progress', created_on=datetime.datetime(2022, 1, 26, 14, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 7%', stats=TwitterTweet.Stats(comments=58, retweets=1306, quotes=146, likes=9676)),
                       TwitterTweet(tweet_id=1485009385403437057, author='year_progress', created_on=datetime.datetime(2022, 1, 22, 22, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 6%', stats=TwitterTweet.Stats(comments=56, retweets=1327, quotes=123, likes=9933)),
                       TwitterTweet(tweet_id=1483680635558453248, author='year_progress', created_on=datetime.datetime(2022, 1, 19, 6, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 5%', stats=TwitterTweet.Stats(comments=55, retweets=1908, quotes=270, likes=12119)),
                       TwitterTweet(tweet_id=1482366981122797570, author='year_progress', created_on=datetime.datetime(2022, 1, 15, 15, 0, tzinfo=datetime.timezone.utc), text='▓░░░░░░░░░░░░░░ 4%', stats=TwitterTweet.Stats(comments=66, retweets=1434, quotes=185, likes=10911)),
                       TwitterTweet(tweet_id=1481038240790593538, author='year_progress', created_on=datetime.datetime(2022, 1, 11, 23, 0, tzinfo=datetime.timezone.utc), text='░░░░░░░░░░░░░░░ 3%', stats=TwitterTweet.Stats(comments=72, retweets=1554, quotes=222, likes=12689)),
                       TwitterTweet(tweet_id=1479724568273211392, author='year_progress', created_on=datetime.datetime(2022, 1, 8, 8, 0, tzinfo=datetime.timezone.utc), text='░░░░░░░░░░░░░░░ 2%', stats=TwitterTweet.Stats(comments=113, retweets=2524, quotes=318, likes=25186)),
                       TwitterTweet(tweet_id=1478395814053568512, author='year_progress', created_on=datetime.datetime(2022, 1, 4, 16, 0, tzinfo=datetime.timezone.utc), text='░░░░░░░░░░░░░░░ 1%', stats=TwitterTweet.Stats(comments=170, retweets=4911, quotes=772, likes=36530))]
    expected_pages = math.ceil(len(expected_result) / Const.Nitter.tweets_per_page)


NonExistingTweetId = "1549959479621324805"


GermanyBlockedTweet = TwitterTweet(
    tweet_id=1168900522092441600,
    author='ShahakShapira',
    created_on=datetime.datetime(2019, 9, 3, 14, 56, tzinfo=datetime.timezone.utc),
    text=base64.b64decode(b'S2lzcyBteSBibGFjayBhc3MgaWhyIEZhc2Noby3DnGJlcnNlaGVyLg==').decode(),
    stats=TwitterTweet.Stats(comments=0, retweets=0, quotes=0, likes=0)
)
