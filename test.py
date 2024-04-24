from bs4 import BeautifulSoup
import requests

def get_full_links_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch webpage")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = [a['href'] for a in soup.find_all('a', href=True)]
    
    article_links = [link for link in links if link.startswith("/wiki/")]
    
    full_links = ['https://en.wikipedia.org' + link for link in article_links]
    
    return full_links


