import requests
import cloudscraper
from bs4 import BeautifulSoup
scraper = cloudscraper.create_scraper()
url = 'https://www.avito.ru/rabota'
r = scraper.get(url)
soup = BeautifulSoup(r.text, "html.parser")

print(soup) 
