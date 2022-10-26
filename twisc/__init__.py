import argparse
from .twisc import scrape


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape tweets.')
    parser.add_argument('--words', type=str, help='Queries. they should be devided by "//" : Cat//Dog.', default=None)
    parser.add_argument('--from_account', type=str, help='Tweets from this account (example : @Tesla).', default=None)
    parser.add_argument('--to_account', type=str, help='Tweets replyed to this account (example : @Tesla).',
                        default=None)
    parser.add_argument('--mention_account', type=str, help='Tweets mention a account (example : @Tesla).',
                        default=None)
    parser.add_argument('--hashtag', type=str, help='Hashtag', default=None)
    parser.add_argument('--until', type=str, help='Max date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--since', type=str, help='Start date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--interval', type=int,
                        help='Interval days between each start date and end date for search queries. example : 5.',
                        default=1)
    parser.add_argument('--lang', type=str, help='Tweets language. example : "en" for english and "fr" for french.',
                        default=None)
    parser.add_argument('--headless', type=bool, help='Headless webdrives or not. True or False', default=False)
    parser.add_argument('--limit', type=int, help='Limit tweets per <interval>', default=float("inf"))
    parser.add_argument('--display_type', type=str, help='Display type of twitter page : Latest or Top', default="Top")
    parser.add_argument('--resume', type=bool, help='Resume the last scraping. specify the csv file path.',
                        default=False)
    parser.add_argument('--proxy', type=str, help='Proxy server', default=None)
    parser.add_argument('--proximity', type=bool, help='Proximity', default=False)
    parser.add_argument('--geocode', type=str, help='Geographical location coordinates to center the search, ' +
                                                    'radius. No compatible with proximity', default=None)
    parser.add_argument('--min_replies', type=int, help='Min. number of replies to the tweet', default=None)
    parser.add_argument('--min_likes', type=int, help='Min. number of likes to the tweet', default=None)
    parser.add_argument('--min_retweets', type=int, help='Min. number of retweets to the tweet', default=None)
    args = parser.parse_args()
    words = args.words
    until = args.until
    since = args.since
    interval = args.interval
    lang = args.lang
    headless = args.headless
    limit = args.limit
    display_type = args.display_type
    from_account = args.from_account
    to_account = args.to_account
    mention_account = args.mention_account
    hashtag = args.hashtag
    resume = args.resume
    proxy = args.proxy
    proximity = args.proximity
    geocode = args.geocode
    min_replies = args.min_replies
    min_likes = args.min_likes
    min_retweets = args.min_likes
    data = scrape(since=since, until=until, words=words, to_account=to_account, from_account=from_account,
                  mention_account=mention_account, hashtag=hashtag, interval=interval, lang=lang, headless=headless,
                  limit=limit, display_type=display_type, resume=resume, proxy=proxy, filter_replies=False,
                  proximity=proximity, geocode=geocode, min_replies=min_replies, min_likes=min_likes,
                  min_retweets=min_retweets)
