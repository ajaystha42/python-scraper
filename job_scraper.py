import requests
from bs4 import BeautifulSoup


def fetch_job_infos(jobs):
    job_details = []
    link_url = 'https://www.linkedin.com/jobs/view/'

    for id in jobs:
        obj = {}
        print(f'Fetching info for job id : {id}')
        obj['job_id'] = id
        job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
        # job_url = f'https://www.linkedin.com/jobs/view/{id}'
        res = requests.get(job_url)
        print('ress:::: ', res.status_code)
        # Bright Data Configuration
        # session = config.setup_requests()
        # res = session.get(target_url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find(
                'h2', class_='top-card-layout__title')
            if title:
                title = title.get_text().strip().upper()
                obj['job_title'] = title
                organization_name = soup.find(
                    'a', class_='topcard__org-name-link')
                if organization_name:
                    company = organization_name.get_text().strip().upper()
                    obj['company'] = company
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
                            obj['link_url'] = link_url + id
                            obj['image'] = image_url
                            obj['linkedin_job_description'] = job_description
                            job_details.append(obj)
                    else:
                        print('job description not found')
                else:
                    print('organization not found')
            else:
                print('title not found')
        else:
            print('Failed to fetch the page.')
    return job_details
