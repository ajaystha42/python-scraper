from selenium.webdriver.common.by import By
import re
import pandas as pd
import config
import jobs_importer
import job_scraper
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


def main():
    driver = config.setup_driver()
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
                driver.execute_script(
                    "arguments[0].click();", modal_close_button)
            company_tag = driver.find_element(
                By.CLASS_NAME, "top-card-layout__cta").get_attribute('href')
            match = re.search(r'f_C=(\d+)', company_tag)
            if company_tag:
                if match:
                    f_c_value = match.group(1)
                    jobids = jobs_importer.import_jobs(f_c_value)
                    total_jobs.append(jobids)
            else:
                print('No See Jobs Element')
        except:
            print(f'No jobs for {company}')
    jobs = [
        element for inner_array in total_jobs for element in inner_array]

    job_details = job_scraper.fetch_job_infos(jobs)
    # jobids = []
    # update in db
    print(len(job_details))
    df = pd.DataFrame(job_details)
    df.to_csv(f'linkedin_jobs.csv',
              index=False, encoding='utf-8')
    print(len(job_details), ' jobs imported.')


if __name__ == "__main__":
    main()
