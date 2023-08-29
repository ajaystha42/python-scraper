import math
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

import constants.urls as urls

# Take f_C from selenium_beautiful_soup.py
# company_code = 165158

#  Running Code
# base_target_url = 'https://www.linkedin.com/jobs/netflix-jobs-worldwide?keywords=Netflix&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0'


def fetch_job_ids(total_jobs, query_params, session):
    job_url = f'{urls.JOB_API_URL}?{query_params}'
    job_ids = set()
    for i in range(0, math.ceil(total_jobs/25)):
        # pagination
        target_url = f'{job_url}&start={i * 25}'
        # res = requests.get(target_url)
        # Bright Data Configuration
        # session = config.setup_requests()
        try:
            res = session.get(target_url)
            if res.status_code == 429:
                # If you receive a 429 status code, sleep for a while before retrying
                # Default to 5 seconds
                wait_time = int(res.headers.get('Retry-After', '5'))
                time.sleep(wait_time)
            else:
                # Raise an exception for non-2xx res
                res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            alljobs_on_this_page = soup.find_all('li')
            for x in range(0, len(alljobs_on_this_page)):
                base_card = alljobs_on_this_page[x].find(
                    'div', {'class': 'base-card'})
                if base_card is not None:
                    jobid = base_card.get('data-entity-urn')
                    if jobid is not None:
                        jobid = jobid.split(':')[3]
                        job_ids.add(int(jobid))
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    return list(job_ids)


def import_jobs(company_code, session):
    # Using Enhanced URL 1
    jobs_search_url = urls.JOBS_SEARCH_URL
    query_params = f'position=1&pageNum=0&f_C={company_code}&f_TPR=r604800&geoId=92000000'
    base_target_url = f'{jobs_search_url}?{query_params}'
    main_res = requests.get(base_target_url)
    main_soup = BeautifulSoup(main_res.text, 'html.parser')
    total_jobs_span = main_soup.find(
        'span', class_='results-context-header__job-count')
    if total_jobs_span:
        total_jobs_text = total_jobs_span.get_text()
        total_jobs_count = ''.join(filter(str.isdigit, total_jobs_text))
        print('Total jobs count:', total_jobs_count)
        n = pd.to_numeric(total_jobs_text)
        job_ids = fetch_job_ids(n, query_params, session)
        return job_ids
    else:
        print('Total jobs span not found.')
