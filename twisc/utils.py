import os
import random
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
import urllib.request as request
import geckodriver_autoinstaller
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from environment import EMAIL, USERNAME, PASSWORD
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_data(card, save_images=False, save_dir=None):
    """
    Extract data from tweet card
    """
    image_links = []
    try:
        username = card.find_element(by=By.XPATH, value='.//span').text
    except:
        return
    try:
        handle = card.find_element(by=By.XPATH, value='.//span[contains(text(), "@")]').text
    except:
        return
    try:
        postdate = card.find_element(by=By.XPATH, value='.//time').get_attribute('datetime')
    except:
        return
    try:
        text = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/div[1]').text
    except:
        text = ""
    try:
        embedded = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/div[2]').text
    except:
        embedded = ""
    try:
        reply_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0
    try:
        retweet_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0
    try:
        like_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="like"]').text
    except:
        like_cnt = 0
    try:
        elements = card.find_elements(by=By.XPATH,
                                      value='.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]')
        for element in elements:
            image_links.append(element.get_attribute('src'))
    except:
        image_links = []
    try:
        promoted = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return
    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements(by=By.XPATH, value='.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    # tweet url
    try:
        element = card.find_element(by=By.XPATH, value='.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return
    tweet = (
        username, handle, postdate, text, embedded, emojis, reply_cnt, retweet_cnt, like_cnt, image_links, tweet_url)
    return tweet


def get_users_follow(users, headless, follow=None, verbose=1, wait=2, limit=float('inf')):
    """
    Get the following or followers of a list of users
    """

    # initiate the driver
    driver = init_driver(headless=headless, firefox=True)
    sleep(wait)
    # log in (the .env file should contain the username and password)
    # driver.get('https://www.twitter.com/login')
    log_in(driver, wait=wait)
    sleep(wait)
    # followers and following dict of each user
    follows_users = {}
    for user in users:
        # if the login fails, find the new log in button and log in again.
        if check_exists_by_link_text("Log in", driver):
            print("Login failed. Retry...")
            login = driver.find_element_by_link_text("Log in")
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            driver.execute_script("arguments[0].click();", login)
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            sleep(wait)
            log_in(driver)
            sleep(wait)
        # case 2
        if check_exists_by_xpath('//input[@name="session[username_or_email]"]', driver):
            print("Login failed. Retry...")
            sleep(wait)
            log_in(driver)
            sleep(wait)
        print("Crawling " + user + " " + follow)
        driver.get('https://twitter.com/' + user + '/' + follow)
        sleep(random.uniform(wait - 0.5, wait + 0.5))
        # check if we must keep scrolling
        scrolling = True
        last_position = driver.execute_script("return window.pageYOffset;")
        follows_elem = []
        follow_ids = set()
        is_limit = False
        while scrolling and not is_limit:
            # get the card of following or followers
            # this is the primary_column attribute that contains both followings and followers
            primary_column = driver.find_element(by=By.XPATH, value='//div[contains(@data-testid,"primary_column")]')
            # extract only the User-cell
            page_cards = primary_column.find_elements(by=By.XPATH, value='//div[contains(@data-testid,"UserCell")]')
            for card in page_cards:
                # get the following or followers element
                element = card.find_element(by=By.XPATH, value='.//div[1]/div[1]/div[1]//a[1]')
                follow_elem = element.get_attribute('href')
                # append to the list
                follow_id = str(follow_elem)
                follow_elem = '@' + str(follow_elem).split('/')[-1]
                if follow_id not in follow_ids:
                    follow_ids.add(follow_id)
                    follows_elem.append(follow_elem)
                if len(follows_elem) >= limit:
                    is_limit = True
                    break
                if verbose:
                    print(follow_elem)
            print("Found " + str(len(follows_elem)) + " " + follow)
            scroll_attempt = 0
            while not is_limit:
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    # end of scroll region
                    if scroll_attempt >= 2:
                        scrolling = False
                        break
                    else:
                        sleep(random.uniform(wait - 0.5, wait + 0.5))  # attempt another scroll
                else:
                    last_position = curr_position
                    break
        follows_users[user] = follows_elem
    return follows_users


def log_in(driver, wait=4):
    driver.get('https://twitter.com/i/flow/login')
    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'
    sleep(random.uniform(wait, wait + 1))
    # enter email
    email_el = driver.find_element(by=By.XPATH, value=email_xpath)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(EMAIL)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    # in case twitter spotted unusual login activity : enter your username
    if check_exists_by_xpath(username_xpath, driver):
        username_el = driver.find_element(by=By.XPATH, value=username_xpath)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(USERNAME)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))
    # enter password
    password_el = driver.find_element(by=By.XPATH, value=password_xpath)
    password_el.send_keys(PASSWORD)
    sleep(random.uniform(wait, wait + 1))
    password_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))


def init_driver(headless=True, proxy=None, show_images=False, option=None, firefox=False):
    """ initiate a chrome driver or firefox driver instance
        option: other option to add (str)
    """
    if firefox:
        options = FirefoxOptions()
        driver_path = geckodriver_autoinstaller.install()
    else:
        options = ChromeOptions()
        driver_path = chromedriver_autoinstaller.install()
    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)
    if not show_images and not firefox:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    if option is not None:
        options.add_argument(option)
    if firefox:
        driver = webdriver.Firefox(options=options, executable_path=driver_path)
    else:
        driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver.set_page_load_timeout(100)
    return driver


def get_last_date_from_csv(path):
    df = pd.read_csv(path)
    return datetime.strftime(max(pd.to_datetime(df["Timestamp"])), '%Y-%m-%dT%H:%M:%S.000Z')


def log_search_page(driver, since, until_local, lang, display_type, words, to_account, from_account, mention_account,
                    hashtag, filter_replies, proximity, geocode, min_replies, min_likes, min_retweets):
    """
    Search by query between since and until_local
    """

    # format the <from_account>, <to_account> and <hash_tags>
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
    mention_account = "(%40" + mention_account + ")%20" if mention_account is not None else ""
    hash_tags = "(%23" + hashtag + ")%20" if hashtag is not None else ""
    if words is not None:
        if len(words) == 1:
            words = "(" + str(''.join(words)) + ")%20"
        else:
            words = "(" + str('%20OR%20'.join(words)) + ")%20"
    else:
        words = ""
    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""
    until_local = "until%3A" + until_local + "%20"
    since = "since%3A" + since + "%20"
    if display_type == "Latest" or display_type == "latest":
        display_type = "&f=live"
    elif display_type == "Image" or display_type == "image":
        display_type = "&f=image"
    else:
        display_type = ""
    # filter replies
    if filter_replies:
        filter_replies = "%20-filter%3Areplies"
    else:
        filter_replies = ""
    # geo
    if geocode is not None:
        geocode = "%20geocode%3A" + geocode
    else:
        geocode = ""
    if min_replies is not None:
        min_replies = "%20min_replies%3A" + str(min_replies)
    else:
        min_replies = ""
    if min_likes is not None:
        min_likes = "%20min_faves%3A" + str(min_likes)
    else:
        min_likes = ""
    if min_retweets is not None:
        min_retweets = "%20min_retweets%3A" + str(min_retweets)
    else:
        min_retweets = ""
    if proximity:
        proximity = "&lf=on"  # at the end
    else:
        proximity = ""
    path = 'https://twitter.com/search?q=' + words + from_account + to_account + mention_account + hash_tags + \
           until_local + since + lang + filter_replies + geocode + min_replies + min_likes + min_retweets + \
           '&src=typed_query' + display_type + proximity
    driver.get(path)
    return path


def keep_scrolling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position,
                   save_images=False):
    """
    Scrolling function for tweets crawling
    """

    save_images_dir = "/images"
    if save_images:
        if not os.path.exists(save_images_dir):
            os.mkdir(save_images_dir)
    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))
        # get the card of tweets
        page_cards = driver.find_elements(by=By.XPATH,
                                          value='//article[@data-testid="tweet"]')  # changed div by article
        for card in page_cards:
            tweet = get_data(card, save_images, save_images_dir)
            if tweet:
                # check if the tweet is unique
                tweet_id = ''.join(tweet[:-2])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.")
                    writer.writerow(tweet)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            scroll += 1
            print("scroll ", scroll)
            sleep(random.uniform(0.5, 1.5))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.5, 1.5))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position


def check_exists_by_link_text(text, driver):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def download_images(urls, save_dir):
    for i, url_v in enumerate(urls):
        for j, url in enumerate(url_v):
            request.urlretrieve(url, save_dir + '/' + str(i + 1) + '_' + str(j + 1) + ".jpg")
