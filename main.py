from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import job_importer

service = Service(executable_path='./chromedriver')
url = 'https://www.linkedin.com/company/netflix/jobs/'
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

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(100)

# headers: {
#     'User-Agent':
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
#     'Accept-Language': 'en-US,en;q=0.9',
# }
driver.get(url)

modal_close_button = driver.find_element(
    "xpath", "//button[@aria-label='Dismiss']")

driver.execute_script("arguments[0].click();", modal_close_button)
company_tag = driver.find_element(
    By.CLASS_NAME, "top-card-layout__cta").get_attribute('href')
match = re.search(r'f_C=(\d+)', company_tag)
if company_tag:
    if match:
        f_c_value = match.group(1)
        print("Company Code :: ", f_c_value)
        # Testing job_importer code
        job_importer.import_jobs(f_c_value)
else:
    print('no such element')

# Now we can use f_c value to fetch all jobs and then
#  use the job ids to fetch its jobs description
