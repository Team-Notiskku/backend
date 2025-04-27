from playwright.sync_api import sync_playwright
from configs.config_keyword_setter import KEYWORD_BASE_URLS
from crawler.modules import generate_hash
from urllib.parse import urljoin
from google.cloud import firestore
from configs.config_firebase import db

def set_notice(keyword):
    base_url = KEYWORD_BASE_URLS.get(keyword)
    xpaths = {
        "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
        "category": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/span[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.skku.edu/skku/campus/skk_comm/notice01.do")
        page.wait_for_load_state("load")

        page.select_option('#search_key', 'article_title')
        page.fill('input[name="srSearchVal"]', keyword)
        page.click('button.sea_btn')
        page.wait_for_load_state('load')

        page_number = 1

        while True:
            print(f"{page_number}페이지 크롤링 중...")

            # 현재 페이지 공지 긁기
            for i in range(1, 11):
                try:
                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
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
                    print(notice_data["title"])
                    print(notice_data["date"])
                    db.collection("notices").document(hash).set(notice_data, merge=True)

                except Exception as e:
                    print(f"공지 {i}개 긁는 중 오류 발생: {e}")
                    continue
            
            if page_number >= 3:
                break

            page_number += 1
            try:
                pager = page.locator('ul.paging') 
                next_page_button = pager.locator('a', has_text=str(page_number))
                next_page_button.click()
                page.wait_for_load_state('load')

            except Exception as e:
                print(f"{page_number}페이지 이동 실패: {e}")
                break

        browser.close()

    print("완료")


for keyword in KEYWORD_BASE_URLS.keys():
    set_notice(keyword)
    print(f"'{keyword}' 크롤링 완료.")