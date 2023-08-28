import requests
from bs4 import BeautifulSoup
import time
import json
import re


def fetch_job_infos(jobs, session):
    job_details = []
    link_url = 'https://www.linkedin.com/jobs/view/'

    for id in jobs:
        data_arr = list()
        id = str(id)
        print(f'Fetching info for job id : {id}')
        job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}'
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
                organization_name = soup.find(
                    'a', class_='topcard__org-name-link')
                if organization_name:
                    company = organization_name.get_text().strip().upper()
                    job_description = soup.find(
                        'div', class_='show-more-less-html__markup')
                    if job_description:
                        prettified_description = job_description.prettify()

                    #     # image = soup.find(
                    #     #     'img', class_='artdeco-entity-image artdeco-entity-image--square-5')
                    #     # if image:
                    #     #     image_url = image.get('data-delayed-url')

                    #     #  Working
                        desc_soup = BeautifulSoup(
                            prettified_description, 'html.parser')
                        # Find all non-br tags and extract their text
                        text_parts = [
                            tag.get_text() for tag in desc_soup.find_all() if tag.name != 'br']

                        # Join the extracted text parts and remove extra spaces
                        # modified_text = re.sub(
                        #     r'\s+', ' ', '\n\n'.join(text_parts))
                        modified_text = '\n'.join(text_parts)

                        # for tag in desc_soup.find_all():

                        #     if tag.name != 'br':
                        #         tag.unwrap()
                        # modified_text = desc_soup.get_text()
                        # print(desc_soup)
                        # print(modified_text)
                        # break
                        lines = [line.strip() for line in modified_text.split(
                            '\n') if line.strip()]
                        collapsed_text = '\n'.join(lines)

                        # Working till here

                        # for br in desc_soup.find_all('br'):
                        #     br.replace_with('\n\n')

                        # # Remove <p> tags
                        # for p in desc_soup.find_all('p'):
                        #     p.extract()

                        # modified_text = desc_soup.get_text()

                        # lines = [line.strip() for line in modified_text.split(
                        #     '\n') if line.strip()]
                        # collapsed_text = '\n'.join(lines)
                        formatted_title = f'Job Title : **{title}**'
                        formatted_company = f'Company : **{company}**'
                        formatted_linkedin_imported_text = f'***JOB IMPORTED FROM LINKEDIN***'

                        data = formatted_linkedin_imported_text + '\n' + \
                            formatted_company + '\n' + formatted_title + '\n' + \
                            collapsed_text + '\n' + link_url + id
                        data_arr.append(data)
                        data_arr.append(json.dumps({'job_id': id}))
                        # obj['image'] = image_url
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
