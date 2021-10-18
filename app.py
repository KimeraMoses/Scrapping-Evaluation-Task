import re
import bs4
import requests
from bs4 import BeautifulSoup

querys = []

def get_links_from_google(query):
    url = 'https://google.com/search?q=' + query
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links

def get_facebook_link(link_list):
    for link in link_list:
        if "facebook" in link:
            return link

def clean_link(any_link):
    if(any_link):
        clean_link = re.search("(?P<url>https?://[^\s]+)", any_link).group("url")
        cleaned_link = clean_link.rsplit('/',1)[0]
        clean_url = cleaned_link + "/about"
        print(clean_url)
        return clean_url
    else:
        print("failed")
        return


def get_companies_from_file():
    with open('company_names.txt') as f:
        for line in f.readlines():
            lines = line.rstrip('\n')
            querys.append(lines)

def main():
    get_companies_from_file()
    for query in querys:
        clean_link(get_facebook_link(get_links_from_google(query)))



if __name__ == "__main__":
    main()











