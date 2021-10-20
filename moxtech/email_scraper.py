import re
import bs4
import requests
from bs4 import BeautifulSoup

querys = []

def google_query(query): 
    url = 'https://google.com/search?q=' + query
    return url


def scrape_generate_links(url):
    try:
        request_result = requests.get(url)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        return links

    except:
        print("no internet connection")
        return

def get_about_link(link_list):
    for link in link_list:
        if "about" in link:
            return link
        
        if "aboutus" in link:
            return link

        if "home" in link:
            return link

        if "contact" in link:
            return link

def clean_link(about_link):
    if(about_link):
        clean_link = re.search("(?P<url>https?://[^\s]+)", about_link).group("url")
        cleaned_link = clean_link.rsplit('/',1)[0]
        print(cleaned_link)
        return cleaned_link

    else:
        print("failed")
        return


def get_contact_from_page(link_list):
    for link in link_list:
        email = re.findall('\S+@\S+', link)
        if(email):
            clean_email = re.sub(r'^.*?:', '', email[0])
            print(clean_email)
            return(clean_email)

def get_companies_from_file():
    with open('company_names.txt') as f:
        for line in f.readlines():
            lines = line.rstrip('\n')
            querys.append(lines)

def write_to_file(company, email):
    with open('company_info.txt', 'a') as f:
        f.write('{0} : {1} \n'.format(company, email))



def main():
    get_companies_from_file()
    for query in querys:
        company_links = clean_link(get_about_link(scrape_generate_links(google_query(query))))
        if(company_links):
            company_email = get_contact_from_page(scrape_generate_links(company_links))
            write_to_file(query, company_email)



if __name__ == "__main__":
    main()

