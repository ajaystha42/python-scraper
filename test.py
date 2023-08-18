# Scraping list of linkedin jobs in a particular field
import requests
# # payload = {'api_key': '64deadbb5df2421883e8d81d', 'field': 'Netflix',
# #            'geoid': '92000000', 'page': '1'}
# payload = {'api_key': '64deadbb5df2421883e8d81d', 'url': 'https://www.linkedin.com/jobs/netflix-jobs-worldwide?keywords=Netflix&location=Worldwide&locationId=&geoId=92000000&f_TPR=r604800&f_C=165158&position=1&pageNum=0',
#            'geoid': '92000000', 'page': '1'}
# resp = requests.get('https://api.scrapingdog.com/scrape', params=payload)
# # resp = requests.get('https://api.scrapingdog.com/linkedinjobs', params=payload)
# print(resp.json())
# arr = resp.json()
# print(len(arr))

# Scraping a particular Linkedin Job Description
'''
https://www.scrapingdog.com/blog/scrape-linkedin-jobs/
'''

payload = {'api_key': '64deadbb5df2421883e8d81d', 'job_id': '3693894486'}
resp = requests.get('https://api.scrapingdog.com/linkedinjobs', params=payload)
print(resp.json())
