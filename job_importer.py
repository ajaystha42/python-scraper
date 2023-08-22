import math

import pandas as pd
import requests
from bs4 import BeautifulSoup


# Take f_C from selenium_beautiful_soup.py
# company_code = 165158

#  Running Code
# base_target_url = 'https://www.linkedin.com/jobs/netflix-jobs-worldwide?keywords=Netflix&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0'


def import_jobs(company_code, jobids):
    # Using Enhanced URL 1
    base_target_url = f'https://www.linkedin.com/jobs/search?position=1&pageNum=0&f_C={company_code}&f_TPR=r604800&geoId=92000000'
    main_res = requests.get(base_target_url)
    main_soup = BeautifulSoup(main_res.text, 'html.parser')
    total_jobs_span = main_soup.find(
        'span', class_='results-context-header__job-count')
    if total_jobs_span:
        total_jobs_text = total_jobs_span.get_text()
        total_jobs_count = ''.join(filter(str.isdigit, total_jobs_text))
        print('Total jobs count:', total_jobs_count)
        # jobids = set()
        n = pd.to_numeric(total_jobs_text)
        query_params = base_target_url.split('?')[1]
        linked_in_job_search_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{query_params}'
        link_url = 'https://www.linkedin.com/jobs/view/'

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
        for id in jobids:
            obj = {}
            print(f'Fetching info for job id : {id}')
            obj['job_id'] = id
            job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
            # job_url = f'https://www.linkedin.com/jobs/view/{id}'
            res = requests.get(job_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find(
                'h2', class_='top-card-layout__title')
            # title = soup.find(
            #     'h1', class_='t-24 t-bold jobs-unified-top-card__job-title')
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
        df = pd.DataFrame(job_details)
        df.to_csv(f'jobs_{company_code}_scraping.csv',
                  index=False, encoding='utf-8')
        print(len(job_details), ' jobs imported.')
    else:
        print('Total jobs span not found.')
