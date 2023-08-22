
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import requests
from bs4 import BeautifulSoup

PROXY_HOST = ''
PROXY_USERNAME = ''
PROXY_PASSWORD = ''
PROXY_PORT = 123


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
    session = requests.Session()
    session.proxies = proxies
    return session
