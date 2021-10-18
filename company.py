import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup


company_url = 'https://www.kfm.co.ug/'
company_name = company_url.split('.')[1]


unprocessed_urls = deque([company_url])

processed_urls = set()

# emails = set()
emails = []

# email_not_found = True

# for email in emails:
#     if company_name in email:
#         email_found = False
#     else: 
#         email_found = True

selected_email = []
while len(unprocessed_urls) and len(emails)< 5:

    url = unprocessed_urls.popleft()
    processed_urls.add(url)

    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    
    print("Scraping %s" % url)
    try:
        results = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue

    company_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", results.text, re.I))
    emails.append(company_emails)

    print(emails)
 
    
    soup = BeautifulSoup(results.text, 'html.parser')

    for anchor in soup.find_all("a"):

        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        if not link in unprocessed_urls and not link in processed_urls:
            unprocessed_urls.append(link)

for email in emails:
    
    if company_name in email:
        selected_email.append(email)
print(selected_email)
