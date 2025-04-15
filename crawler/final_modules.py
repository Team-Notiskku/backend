from playwright.sync_api import sync_playwright
from configs.config_common import XPATH, BASE_URL
from configs.config_department import DEPT_XPATHS, DEPT_URLS, pin_dept
from configs.config_major import MAJOR_XPATHS, MAJOR_URLS, pin_major
from configs.config_firebase import db
from urllib.parse import urljoin
from google.cloud import firestore
import re
import hashlib

def generate_hash(type, department, major, title, uploader):
    key = f"{type.strip()}|{(department or '').strip()}|{(major or '').strip()}|{title.strip()}|{(uploader or '').strip()}"
    return hashlib.md5(key.encode()).hexdigest()

def get_xpath(type, department, major):
    if type == "전체":
        return XPATH 
    elif type == "단과대":
        return DEPT_XPATHS.get(department, {})
    elif type == "학과":
        return MAJOR_XPATHS.get(major, {})  
    else:
        raise ValueError(f"알 수 없는 공지: {type, department, major}")
    
def get_base_url(type, department, major):
    if type == "전체":
        return BASE_URL
    elif type == "단과대":
        return DEPT_URLS.get(department, "")
    elif type == "학과":
        return MAJOR_URLS.get(major, "")  
    else:
        raise ValueError(f"알 수 없는 공지: {type, department, major}")\
        
def get_notice(type, department, major, max_pages):
    base_url = get_base_url(type, department, major)
    xpaths = get_xpath(type, department, major)
    
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
                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    if xpaths["views"] != "" :
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    else:
                        views = 'null'
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")
                    link = urljoin(base_url, link)

                    ## hash (title + uploader)
                    hash = generate_hash(type, department, major, title, uploader)

                    ## id 필드 뺐음
                    notice_data = {
                        "type": type,
                        "department": department,
                        "major": major,
                        "title": title,
                        "category": category,
                        "uploader": uploader,
                        "date": date,
                        "views": views,
                        "url": link,
                        "updated_at": firestore.SERVER_TIMESTAMP,
                    }
                    ## DB 저장
                    db.collection("notices").document(hash).set(notice_data, merge=True)

                except Exception as e:
                    print(f"[{type} - {department} - {major}] {i-1}번 공지 이후로 크롤링 종료됨. Error: {e}")
                    browser.close()
                    return

        browser.close()