from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.avito.ru/all/vakansii?utm_campaign=print&utm_medium=redirect&utm_source=ooh')
    sleep(5)
    
    # Получаем HTML код страницы
    html = page.content()
    
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    print(html)
    browser.close()