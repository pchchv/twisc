import io
import os
import setuptools
from distutils.core import setup
from twisc import __version__ as version


# Long description
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = '\n' + f.read()


setup(
  name=version.__title__,
  packages=[version.__title__],
  version=version.__version__,
  license=version.__license__,
  description=version.__description__,
  long_description=readme,
  long_description_content_type='text/markdown',
  author=version.__author__,
  author_email=version.__contact__,
  url=version.__url__,
  download_url=version.__url__,
  keywords=['twitter', 'scraper', 'python', "crawl", "following", "followers", "twitter-scraper", "tweets"],
  install_requires=['selenium', 'pandas', 'python-dotenv', 'chromedriver-autoinstaller', 'urllib3'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
