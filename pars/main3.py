from playwright.sync_api import sync_playwright
from time import sleep

def run(user_id, url):

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)
        time.sleep(11)

        html_content = page.content()

        while True:
            page.goto(url)
            time.sleep(25)

            html_content = page.content()

            if "Робот или человек?" not in html_content:
                break

            print("Робот или человек?")

            page.reload(waitUntil="domcontentloaded")
            time.sleep(15)

        block_list = load_block_list()

        while True:
            time.sleep(5)
            elements = page.query_selector_all('[data-test-component="ProductOrAdCard"]')

            for element in elements[3:]:
                try:
                    href = element.eval_on_selector('span > a', 'a => a.href')

                    if href in block_list:
                        print(f"in blacklist")
                        continue

                    text = element.eval_on_selector('span > a', 'a => a.title')
                    html_content = element.inner_html()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    price_element = soup.select_one('span.sc-ejxegM.jZqcnD')
                    price = price_element.text.strip()

                    item_id = extract_id_from_url(href)
                    image_src = element.eval_on_selector(
                        'figure > div > div > svg > image',
                        'image => image.getAttribute("xlink:href")'
                    )
                    print(f"Href: {href}, Text: {text}")

                    bot.send_photo(user_id, photo=image_src, caption=f'!Нашлась карточка товара!\n'
                                                                             f'Имя товара: {text}\n'
                                                                             f'Цена товара: {price}\n'
                                                                             f'ID: {item_id}\n'
                                                                             f'<a href="{href}">Перейти на товар</a>',
                                   parse_mode='HTML')

                    block_list.add(href)

                except Exception as e:
                    continue

            save_block_list(block_list)

            page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
            page.goto(url)

            new_elements = page.query_selector_all('[data-test-component="ProductOrAdCard"]')
            if not new_elements:
                break

        browser.close()