import pandas as pd
from datetime import datetime
from selenium import webdriver
import geckodriver_autoinstaller
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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
