from selenium import webdriver
import time
import pandas as pd
import os

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3674700593&f_C=165158&f_TPR=r604800&geoId=92000000'
# 'https://www.linkedin.com/jobs/search/?currentJobId=3694026977&f_C=2920773&geoId=92000000&originToLandingJobPostings=3667404708%2C3669264653%2C3667153500%2C3668081092%2C3667156194%2C3668078267%2C3667812068%2C2825608196%2C3018262160&position=4&pageNum=0'
#
service = Service(executable_path='./chromedriver')
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
driver.get(url1)

y = driver.find_elements(
    By.CLASS_NAME, "results-context-header__job-count")[0].text


n = pd.to_numeric(y)
print(n)
# results-context-header__job-count

# Loop to scroll through all jobs and click on see more jobs button for infinite scrolling

i = 2
while i <= int((n+200)/25)+1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1

    try:
        send = driver.find_element(
            "xpath", "//button[@aria-label='Load more results']")

        driver.execute_script("arguments[0].click();", send)
        time.sleep(3)

        # buu=driver.find_elements_by_tag_name("button")
        # x=[btn for btn in buu if btn.text=="See more jobs"]
        # for btn in x:
        # driver.execute_script("arguments[0].click();", btn)
        # time.sleep(3)

    except:
        pass
        time.sleep(5)
print('all doneeeeea')
companyname = []
titlename = []


# Find company name and append it to the blank list

# try:
# for i in range(n):
#     company = driver.find_elements(
#         By.CLASS_NAME, "base-search-card__subtitle")[i].text

#     companyname.append(company)
companies = driver.find_elements(
    By.CLASS_NAME, "base-search-card__subtitle")
for company in companies:
    companyname.append(company.text)
print('companieesss', companyname)
print(len(companyname))
# except IndexError:
#     print("no")

# Find title name and append it to the blank list
try:
    titles = driver.find_elements(
        By.CLASS_NAME, "base-search-card__title")
    for title in titles:
        titlename.append(title.text)
    print('companieesss', companyname)
    print(len(companyname))

    print('titless ', titlename)
    print(len(titlename))

except IndexError:
    print("no")


# Create dataframe for company name and title

companyfinal = pd.DataFrame(companyname, columns=["company"])
titlefinal = pd.DataFrame(titlename, columns=["title"])

# Join the two lists

x = companyfinal.join(titlefinal)

# Save file in your directory
x.to_csv('linkedin.csv')
