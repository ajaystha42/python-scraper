import requests
from bs4 import BeautifulSoup

import math
import pandas as pd

companies = ['Netflix', 'Fusemachines']

base_target_url = 'https://www.linkedin.com/jobs/netflix-jobs-worldwide?keywords=Netflix&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0'
main_res = requests.get(base_target_url)
main_soup = BeautifulSoup(main_res.text, 'html.parser')

#  search url
# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0&start=50

total_jobs_span = main_soup.find(
    'span', class_='results-context-header__job-count')
if total_jobs_span:
    # Get the full text content of the span
    total_jobs_text = total_jobs_span.get_text()
    # Extract numeric digits
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
        alljobs_on_this_page = soup.find_all("li")
        for x in range(0, len(alljobs_on_this_page)):
            base_card = alljobs_on_this_page[x].find(
                "div", {"class": "base-card"})
            if base_card is not None:
                jobid = base_card.get('data-entity-urn')
                if jobid is not None:
                    jobid = jobid.split(":")[3]
                    jobids.add(jobid)
    job_details = []
    job_ids_list = list(jobids)

    o = {}
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(0, len(job_ids_list)):
        resp = requests.get(target_url.format(job_ids_list[j]))
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            o["company"] = soup.find(
                "div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
            o["job-title"] = soup.find(
                "div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
            o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find(
                "li").text.replace("Seniority level", "").strip()
        except:
            pass

        job_details.append(o)
        o = {}

    # for id in jobids:
    #     obj = {}
    #     print(f'Fetching info for job id = {id}')
    #     obj['job_id'] = id
    #     job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
    #     res = requests.get(job_url)
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     title = soup.find(
    #         'h2', class_='top-card-layout__title')
    #     if title:
    #         title = title.get_text().strip()
    #         obj['title'] = title
    #         organization_name = soup.find(
    #             'a', class_='topcard__org-name-link')
    #         if organization_name:
    #             company = organization_name.get_text().strip()
    #             print(company)
    #             obj['company'] = company
    #             job_description = soup.find(
    #                 'div', class_='show-more-less-html__markup')
    #             if job_description:
    #                 job_description = job_description.get_text().strip()
    #                 obj['job_description'] = job_description
    #             else:
    #                 print('job description not found')
    #                 break
    #         else:
    #             print('organization not found')
    #             break
    #     else:
    #         print('title not found')
    #         break
    #     job_details.append(obj)
    print(job_details)
    print(len(job_details))
    df = pd.DataFrame(job_details)
    df.to_csv('linkedinjobs_scraping.csv', index=False, encoding='utf-8')
else:
    print('Total jobs span not found.')
