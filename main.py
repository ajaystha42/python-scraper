from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import job_importer


'''
Url 1 : https://www.linkedin.com/jobs/search?keywords=Netflix&location=&geoId=&f_TPR=r604800&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0

f_TPR for past 1 week results - can be hardcoded
f_C - for company - needs to be DYNAMIC 
Filtered Url 1 = https://www.linkedin.com/jobs/search?keywords=&location=&geoId=&position=1&pageNum=0&f_C=165158&f_TPR=r604800

Enhanced Url 1 = https://www.linkedin.com/jobs/search?position=1&pageNum=0&f_C=165158&f_TPR=r604800&geoId=92000000
in jobs page of each company, theres a See All Jobs where we can find f_c (company_id)from where we can search
for apis directly in filtered url 1

geoId=92000000 for WORLDWIDE
by default USA

'''
companies = ['netflix', 'fusemachines',
             'warner-bros--entertainment', 'marvel-studios'
             ]

# service = Service(executable_path='./chromedriver')
# url = 'https://www.linkedin.com/company/netflix/jobs/'
options = Options()
# options.add_experimental_option("detach", True)


# Proxy Bright Data Configuration
# options.add_argument('--proxy-server=http://%s:%s@%s:%s' %
#                      (proxy_username, proxy_password, proxy_host, str(proxy_port)))
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")


# Run Chrome in headless mode
# options.add_argument('--headless')


# Disable GPU acceleration
# options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    # service=service,
    options=options
)
driver.implicitly_wait(10)

# headers: {
#     'User-Agent':
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
#     'Accept-Language': 'en-US,en;q=0.9',
# }
for company in companies:
    try:
        jobids = set()

        print(f'Fetching Job Informations for Company : {company}')
        # driver.get(f'https://www.linkedin.com/company/{company}/jobs/')
        driver.get(f'https://www.linkedin.com/company/{company}/')

        modal_close_button = driver.find_element(
            "xpath", "//button[@aria-label='Dismiss']")
        if modal_close_button:
            driver.execute_script("arguments[0].click();", modal_close_button)
        company_tag = driver.find_element(
            By.CLASS_NAME, "top-card-layout__cta").get_attribute('href')
        match = re.search(r'f_C=(\d+)', company_tag)
        if company_tag:
            if match:
                f_c_value = match.group(1)
                print("Company Code :: ", f_c_value)
                # Testing job_importer code
                job_importer.import_jobs(f_c_value, jobids)
        else:
            print('No See Jobs Element')
    except:
        print(f'No jobs for {company}')

# Now we can use f_c value to fetch all jobs and then
#  use the job ids to fetch its jobs description
