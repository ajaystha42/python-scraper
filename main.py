from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import job_importer
import pandas as pd
import requests
from bs4 import BeautifulSoup


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

# headers: {
#     'User-Agent':
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
#     'Accept-Language': 'en-US,en;q=0.9',
# }

# total_jobs = [['3698260330', '3701051286', '3691231651', '3698256616',
#               '3698262028', '3698260328', '3698255995', '3698255996']]

total_jobs = list()
url = 'https://www.linkedin.com/company'
for company in companies:
    try:
        print(f'Fetching Job Informations for Company : {company}')
        # driver.get(f'https://www.linkedin.com/company/{company}/jobs/')
        driver.get(f'{url}/{company}/')

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
                # Testing job_importer code
                jobids = job_importer.import_jobs(f_c_value)
                total_jobs.append(jobids)
        else:
            print('No See Jobs Element')
    except:
        print(f'No jobs for {company}')

job_details = []
link_url = 'https://www.linkedin.com/jobs/view/'
jobs = [
    element for inner_array in total_jobs for element in inner_array]
for id in jobs:
    obj = {}
    print(f'Fetching info for job id : {id}')
    obj['job_id'] = id
    job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
    # job_url = f'https://www.linkedin.com/jobs/view/{id}'
    res = requests.get(job_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find(
        'h2', class_='top-card-layout__title')
    if title:
        title = title.get_text().strip()
        obj['title'] = title
        organization_name = soup.find(
            'a', class_='topcard__org-name-link')
        if organization_name:
            company = organization_name.get_text().strip()
            obj['company'] = company
            job_description = soup.find(
                'div', class_='show-more-less-html__markup')
            if job_description:
                job_description = job_description.get_text().strip()
                obj['job_description'] = job_description
                image = soup.find(
                    'img', class_='artdeco-entity-image artdeco-entity-image--square-5')
                if image:
                    image_url = image.get('data-delayed-url')
                    obj['link_url'] = link_url + id
                    obj['image'] = image_url
                    job_details.append(obj)
            else:
                print('job description not found')
        else:
            print('organization not found')
    else:
        print('title not found')
        # jobids = []
        # update in db
print(len(job_details))
df = pd.DataFrame(job_details)
df.to_csv(f'linkedin_jobs.csv',
          index=False, encoding='utf-8')
print(len(job_details), ' jobs imported.')
