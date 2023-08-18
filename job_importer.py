import json
import math
import re
from html import unescape

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

companies = ['Netflix', 'Fusemachines']

'''
Url 1 : https://www.linkedin.com/jobs/search?keywords=Netflix&location=&geoId=&f_TPR=r604800&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0

f_TPR for past 1 week results - can be hardcoded
f_C - for company - needs to be DYNAMIC 
Filtered Url 1 = https://www.linkedin.com/jobs/search?keywords=&location=&geoId=&position=1&pageNum=0&f_C=165158&f_TPR=r604800

Enhanced Url 1 = https://www.linkedin.com/jobs/search?position=1&pageNum=0&f_C=165158&f_TPR=r604800
in jobs page of each company, theres a See All Jobs where we can find f_c (company_id)from where we can search
for apis directly in filtered url 1

geoId=92000000 for WORLDWIDE
by default USA

'''


#  Running Code
base_target_url = 'https://www.linkedin.com/jobs/netflix-jobs-worldwide?keywords=Netflix&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0'
main_res = requests.get(base_target_url)
main_soup = BeautifulSoup(main_res.text, 'html.parser')
print(main_soup)
total_jobs_span = main_soup.find(
    'span', class_='results-context-header__job-count')
if total_jobs_span:
    total_jobs_text = total_jobs_span.get_text()
    total_jobs_count = ''.join(filter(str.isdigit, total_jobs_text))
    print('Total jobs count:', total_jobs_count)
    jobids = set()
    n = pd.to_numeric(total_jobs_text)
    query_params = base_target_url.split('?')[1]
    linked_in_job_search_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{query_params}'
    for i in range(0, math.ceil(n/25)):
        # pagination
        target_url = f'{linked_in_job_search_url}&start={i * 25}'
        res = requests.get(target_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all('li')
        for x in range(0, len(alljobs_on_this_page)):
            base_card = alljobs_on_this_page[x].find(
                'div', {'class': 'base-card'})
            if base_card is not None:
                jobid = base_card.get('data-entity-urn')
                if jobid is not None:
                    jobid = jobid.split(':')[3]
                    jobids.add(jobid)
    job_details = []
    print(jobids)
    for id in jobids:
        obj = {}
        print(f'Fetching info for job id = {id}')
        obj['job_id'] = id
        job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
        res = requests.get(job_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find(
            'h2', class_='top-card-layout__title')
        # title = soup.find(
        #     'div', {'class': 'top-card-layout__entity-info'}).find('a').text.strip()
        if title:
            title = title.get_text().strip()
            obj['title'] = title
            organization_name = soup.find(
                'a', class_='topcard__org-name-link')
            # organization_name = soup.find(
            #     'div', {'class': 'top-card-layout__card'}).find('a').find('img').get('alt')
            if organization_name:
                company = organization_name.get_text().strip()
                print(company)
                obj['company'] = company
                job_description = soup.find(
                    'div', class_='show-more-less-html__markup')
                if job_description:
                    job_description = job_description.get_text().strip()
                    obj['job_description'] = job_description
                    job_details.append(obj)
                else:
                    print('job description not found')
            else:
                print('organization not found')
        else:
            print('title not found')

    print(job_details)
    print(len(job_details))
    df = pd.DataFrame(job_details)
    df.to_csv('linkedinjobs_scraping.csv', index=False, encoding='utf-8')
else:
    print('Total jobs span not found.')
