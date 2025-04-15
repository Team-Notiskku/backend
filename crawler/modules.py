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
            if department == "약학대학":
                cur_page = page_num+1
                full_url = f"{base_url}&page={cur_page}#subcon"
            elif department == "의과대학":
                cur_page = page_num+1
                notice_url = f"?keyword=&startpage=1&bcode=nt&pg={cur_page}"
                full_url = urljoin(base_url, notice_url)
            else: 
                offset = page_num * 10
                notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
                full_url = urljoin(base_url, notice_url)
            
            page.goto(full_url)
            page.wait_for_load_state("load")

            pinned_count = 0

            if department in pin_dept or major in pin_major:
                if major == "건축학과(건축학계열)":
                    pinned_notices = page.locator('//*[@id="item_body"]/div[2]/div[1]/div/div[2]/div/div/div/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
                else:
                    pinned_notices = page.locator('//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
                pinned_count = pinned_notices.count()  # 고정 공지 개수
            
            notice_count = 0
            i = pinned_count+1
            
            per_page = 10
            while notice_count < per_page:
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
                    
                    if department == "약학대학":
                        match = re.match(r"^\d+\.\s*", title)
                        if match:
                            title = title[match.end():]
                    
                    if department == "의과대학":
                        views = views[4:]

                    if major == "화학과":
                        date = date[14:]
                        views = views[6:]

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
                    notice_count+=1
                    i+=1

                except Exception as e:
                    print(f"[{type} - {department} - {major}] {i-1}번 공지 이후로 크롤링 종료됨. Error: {e}")
                    browser.close()
                    return

        browser.close()