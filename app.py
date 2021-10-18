import re
import bs4
import requests
from bs4 import BeautifulSoup as Soup



def get_links_from_google(query):
    url = 'https://google.com/search?q=' + query
    request_result = requests.get(url)
    soup = Soup(request_result.text, "html.parser")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links

def get_facebook_link(link_list):
    for link in link_list:
        if "facebook" in link:
            return link

company_fb_url =[]
def clean_link(scraped_co_link):
    if(scraped_co_link):
        clean_link = re.search("(?P<url>https?://[^\s]+)", scraped_co_link).group("url")
        cleaned_link = clean_link.rsplit('/',1)[0]
        clean_url = cleaned_link + "/about"
        print(clean_url)
        company_fb_url.append(clean_url)
        return clean_url
    else:
        print("failed")
        return

querys = []

def get_companies_from_file():
    with open('company_names.txt') as f:
        for line in f.readlines():
            lines = line.rstrip('\n')
            querys.append(lines)

def main():
    get_companies_from_file()
    for query in querys:
        clean_link(get_facebook_link(get_links_from_google(query)))
    print(company_fb_url)


if __name__ == "__main__":
    main()

def get_company_email_from_fb():
    for url in company_fb_url:
        fb_request_result = requests.get(url)
        soup = Soup(fb_request_result.text, "html.parser")
        email_container = soup.findAll('a', class_="j83agx80")
        email = email_container.text 
        print(email)
    
get_company_email_from_fb()










