
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def setup_driver():
    # service = Service(executable_path='./chromedriver')
    options = Options()
    # options.add_experimental_option("detach", True)

    proxy_host = ''
    proxy_username = ''
    proxy_password = ''
    proxy_port = 123
    # Proxy Bright Data Configuration
    # options.add_argument('--proxy-server=http://%s:%s@%s:%s' %
    #                      (proxy_username, proxy_password, proxy_host, str(proxy_port)))
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
