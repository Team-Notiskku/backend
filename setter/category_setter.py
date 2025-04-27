from playwright.sync_api import sync_playwright
from configs.config_common_categories import CATEGORY_BASE_URLS
from crawler.modules import generate_hash
from urllib.parse import urljoin
from google.cloud import firestore
from configs.config_firebase import db

def set_notice(category):
    base_url = CATEGORY_BASE_URLS.get(category)
    xpaths = {
    "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
    "id": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[1]',
    "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
    "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
    "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
    "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        offset = page_num * 10
        notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
        full_url = urljoin(base_url, notice_url)

        for page_num in (10):
            page.goto(full_url)
            page.wait_for_load_state("load")

            notice_count = 0
            i = 1
            per_page = 10

            while notice_count < per_page:
                try:
                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    link = urljoin(base_url, page.locator(xpaths["link"].format(i)).get_attribute("href"))


                    hash = generate_hash("전체", None, None, title, uploader)

                    notice_data = {
                        "type": "전체",
                        "title": title,
                        "category": category,
                        "uploader": uploader,
                        "date": date,
                        "views": views,
                        "url": link,
                        "updated_at": firestore.SERVER_TIMESTAMP,
                    }
                    db.collection("notices").document(hash).set(notice_data, merge=True)
                    notice_count += 1
                    i += 1

                except Exception as e:
                    print("오류")
                    browser.close()
                    return

        browser.close()

    print("완료")


for category in CATEGORY_BASE_URLS.keys():
    set_notice(category)
    print(category)