import requests
from bs4 import BeautifulSoup
url = 'http://www.thebetterindia.com/topics/blog/'
def crawl(url):
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text)
    for link in soup.find_all('a',{'rel':'bookmark'}):
        title = link.string
        print(title + '\n')
    for lin in soup.find_all('a',{'class':'g1-button g1-button-m g1-button-solid g1-load-more','href':'#'}):
        href = lin.get('data-g1-next-page-url')
        #print(href)
        crawl(href)
crawl(url)