import requests
from bs4 import BeautifulSoup
import time


def fetch_job_infos(jobs, session):
    job_details = []
    link_url = 'https://www.linkedin.com/jobs/view/'

    for id in jobs:
        obj = {}
        data_arr = list()
        id = str(id)
        print(f'Fetching info for job id : {id}')
        # obj['job_id'] = str(id)
        job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
        # job_url = f'https://www.linkedin.com/jobs/view/{id}'
        # res = requests.get(job_url)
        # Bright Data Configuration
        # session = config.setup_requests()
        # res = session.get(target_url)
        try:
            res = session.get(job_url)
            if res.status_code == 429:
                # If you receive a 429 status code, sleep for a while before retrying
                # Default to 5 seconds
                # wait_time = int(res.headers.get('Retry-After', '5'))
                time.sleep(5)
            else:
                # Raise an exception for non-2xx res
                res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find(
                'h2', class_='top-card-layout__title')
            if title:
                title = title.get_text().strip().upper()
                # obj['job_title'] = title
                organization_name = soup.find(
                    'a', class_='topcard__org-name-link')
                if organization_name:
                    company = organization_name.get_text().strip().upper()
                    # obj['company'] = company
                    job_description = soup.find(
                        'div', class_='show-more-less-html__markup')
                    if job_description:
                        job_description = job_description.get_text().strip()

                        image = soup.find(
                            'img', class_='artdeco-entity-image artdeco-entity-image--square-5')
                        if image:
                            image_url = image.get('data-delayed-url')

                            # For testing
                            obj['description'] = 'JOB IMPORTED FROM LINKEDIN \n' + \
                                company + '\n' + title + '\n' + job_description
                            data_arr.append('JOB IMPORTED FROM LINKEDIN \n' +
                                            company + '\n' + title + '\n' + job_description)
                            data_arr.append(511)
                            # data_arr.append(2)
                            # obj['link_url'] = link_url + id
                            # obj['image'] = image_url
                            # obj['linkedin_job_description'] = job_description

                            # job_details.append(obj)
                            job_details.append(tuple(data_arr))
                    else:
                        print('job description not found')
                else:
                    print('organization not found')
            else:
                print(f'Title not found for Job Id: {id}')
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    return job_details
