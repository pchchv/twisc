import datetime


def scrape(since, until=None, interval=5):
    """
    Scrape data from twitter using requests.
    Starting from <since> until <until>.
    The application make a search between each <since> and <until_local>
    until it reaches the <until> date if it's given, else it stops at the actual date.
    Return:
        data containing all tweets scraped with the associated features.
    Save a CSV file containing all tweets scraped with the associated features.
    """

    # header of csv
    header = [
        'UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text',
        'Emojis', 'Comments', 'Likes', 'Retweets', 'Image link', 'Tweet URL'
    ]
    data = []
    tweet_ids = set()
    write_mode = 'w'
    # start scraping from <since> until <until>
    # add the <interval> to <since> to get <until_local> for the first refresh
    until_local = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
    if until is None:
        # set until to the actual date
        until = datetime.date.today().strftime("%Y-%m-%d")
    # set refresh at 0. we refresh the page for each <interval> of time
    refresh = 0
