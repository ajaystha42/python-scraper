from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import requests
import re
# Set up Chrome options to run headless
service = Service(executable_path='./chromedriver')
url = 'https://www.linkedin.com/company/marvel-studios/jobs/'
options = Options()
options.add_experimental_option("detach", True)

# Run Chrome in headless mode
# options.add_argument('--headless')
# Disable GPU acceleration
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
driver.get(url)

send = driver.find_element(
    "xpath", "//button[@aria-label='Dismiss']")

driver.execute_script("arguments[0].click();", send)

x = driver.find_element(
    By.CLASS_NAME, "top-card-layout__cta").get_attribute('href')
match = re.search(r'f_C=(\d+)', x)
if match:
    f_c_value = match.group(1)
    print("f_C value:", f_c_value)

# Now we can use f_c value to fetch all jobs and then
#  use the job ids to fetch its jobs description
