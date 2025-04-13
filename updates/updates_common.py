from configs.config_common import BASE_URL, XPATH
from configs.config_firebase import db
from crawler.crawler_common import generate_notice_hash
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from google.cloud import firestore

def update_common(base_url, xpaths):
    max_pages = 2 ## 최대 20개까지 로딩

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            page.goto(full_url)
            page.wait_for_load_state("load")

            for i in range(1, 11):
                try:
                    notice_type = "전체 공지"
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    id = id[3:]
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"
                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")
                    link = urljoin(base_url, link)

                    ## hash (title + uploader)
                    hash = generate_notice_hash(notice_type, title, uploader)

                    ## id 필드 뺐음
                    notice_data = {
                        "type": notice_type,
                        "title": title,
                        "category": category,
                        "uploader": uploader,
                        "date": date,
                        "views": views,
                        "url": link,
                        "created_at": firestore.SERVER_TIMESTAMP,
                        "is_pushed": False
                    }

                    ## DB 저장
                    db.collection("notices").document(hash).set(notice_data, merge=True)

                except Exception as e:
                    browser.close()
                    return

        browser.close()

update_common(BASE_URL, XPATH)
print("업데이트가 완료되었습니다. 종료합니다.")