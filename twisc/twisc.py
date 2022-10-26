import os
import datetime
from utils import init_driver, get_last_date_from_csv


def scrape(since, until=None, init_date=None, max_date=None, words=None, to_account=None, from_account=None,
           mention_account=None, interval=5, headless=True, resume=False, proxy=None, hashtag=None, show_images=False,
           save_images=False, save_dir="outputs"):
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
    # file path
    if words:
        if type(words) == str:
            words = words.split("//")
        path =\
            save_dir + "/" + '_'.join(words) + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[0] + '.csv'
    elif from_account:
        path = \
            save_dir + "/" + from_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[0] + '.csv'
    elif to_account:
        path = \
            save_dir + "/" + to_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[0] + '.csv'
    elif mention_account:
        path = \
            save_dir + "/" + mention_account + '_' + str(init_date).split(' ')[0] + '_' + \
            str(max_date).split(' ')[0] + '.csv'
    elif hashtag:
        path = \
            save_dir + "/" + hashtag + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[0] + '.csv'
    # create the <save_dir>
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # show images during scraping (for saving purpose)
    if save_images:
        show_images = True
    # initiate the driver
    driver = init_driver(headless, proxy, show_images)
    # resume scraping from previous work
    if resume:
        since = str(get_last_date_from_csv(path))[:10]
        write_mode = 'a'
