"""
Retrieving data from an environment file
"""


import os
from dotenv import load_dotenv


load_dotenv('/.env')


EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAME')
