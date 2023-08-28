
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import psycopg2
from psycopg2 import Error


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROXY_HOST = ''
PROXY_USERNAME = ''
PROXY_PASSWORD = ''
PROXY_PORT = 123

# FOR LOCAL DB
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USERNAME = 'postgres'
DB_PASSWORD = 'Aj@y'
DB_NAME = 'husslup'


def setup_driver():
    # service = Service(executable_path='./chromedriver')
    options = Options()
    # options.add_experimental_option("detach", True)

    # Proxy Bright Data Configuration
    # options.add_argument('--proxy-server=http://%s:%s@%s:%s' %
    #                      (PROXY_USERNAME, PROXY_PASSWORD, PROXY_HOST, str(PROXY_PORT)))
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    # Run Chrome in headless mode
    options.add_argument('--headless')

    # Disable GPU acceleration
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        # service=service,
        options=options
    )
    driver.implicitly_wait(10)
    return driver


def setup_requests():
    proxies = {
        "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{str(PROXY_PORT)}",
        "https": f"https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{str(PROXY_PORT)}",
    }

    retry_strategy = Retry(
        total=3,  # Number of retries
        # HTTP error codes to retry on
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=0.5,  # Factor to increase delay between retries
    )

    session = requests.Session()
    # session.proxies = proxies
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def create_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            port=str(DB_PORT)
        )
        print("Connected to the database successfully")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
