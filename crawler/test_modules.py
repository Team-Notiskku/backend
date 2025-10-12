
from playwright.sync_api import sync_playwright
from configs.config_common import XPATH, BASE_URL
from configs.config_department import DEPT_XPATHS, DEPT_URLS, pin_dept
from configs.config_major import MAJOR_XPATHS, MAJOR_URLS, pin_major
from urllib.parse import urljoin
from configs.config_topic_map import mapper
import re
import hashlib

def send_notice(keywords, title):
    for keyword in keywords:
        mapped_topic = mapper[keyword]
        topic_type = mapped_topic[0:2]
        topic_details = mapped_topic[2:4]

        if topic_type == "00":
            message = messaging.Message(
                data={
                    "title": title,
                    "body": f"‘{keyword}’ 관련 공지가 새로 업데이트 되었어요!",
                },
                topic=topic_details
            )
            # 실제 전송
            response = messaging.send(message)
            print("전송 완료:", response)

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

def clean_notice_fields(department, major, title, date, views):
    if department == "약학대학":
        match = re.match(r"^\d+\.\s*", title)
        if match:
            title = title[match.end():]
    if department == "의과대학":
        views = views[4:]
    if major == "화학과":
        date = date[14:]
        views = views[6:]

def generate_hash(type, department, major, title, uploader):
    key = f"{type.strip()}|{(department or '').strip()}|{(major or '').strip()}|{title.strip()}|{(uploader or '').strip()}"
    return hashlib.md5(key.encode()).hexdigest()

def try_or_default(func, default):
    try:
        return func() 
    except:
        return default

def get_views(page, xpaths, i):
    return page.locator(xpaths["views"].format(i)).inner_text(timeout=1000) if xpaths["views"] else 'null'

def get_notice(type, department, major, max_pages):
    base_url = get_base_url(type, department, major)
    xpaths = get_xpath(type, department, major)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            # 페이지 URL 구성
            if department == "약학대학":
                cur_page = page_num + 1
                full_url = f"{base_url}&page={cur_page}#subcon"
            elif department == "의과대학":
                cur_page = page_num + 1
                notice_url = f"?keyword=&startpage=1&bcode=nt&pg={cur_page}"
                full_url = urljoin(base_url, notice_url)
            else:
                offset = page_num * 10
                notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
                full_url = urljoin(base_url, notice_url)

            page.goto(full_url)
            page.wait_for_load_state("load")

            if department in pin_dept or major in pin_major:
                if major == "건축학과(건축학계열)":
                    pinned_notices = page.locator(
                        '//*[@id="item_body"]/div[2]/div[1]/div/div[2]/div/div/div/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
                else:
                    pinned_notices = page.locator(
                        '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
                pinned_count = pinned_notices.count()

                for i in range(1, pinned_count + 1):
                    try:
                        title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                        category = try_or_default(lambda: page.locator(xpaths["category"].format(i)).inner_text(timeout=1000), "없음")
                        uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                        date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                        views = get_views(page, xpaths, i)
                        link = urljoin(base_url, page.locator(xpaths["link"].format(i)).get_attribute("href"))

                        clean_notice_fields(department, major, title, date, views)

                        hash = generate_hash(type, department, major, title, uploader)

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
                            "isPinned": True
                        }
                        print(notice_data[title])
                    except Exception as e:
                        print(f"[{type} - {department} - {major}] 고정공지 {i}번 에러: {e}")

            notice_count = 0
            i = (pinned_count if department in pin_dept or major in pin_major else 0) + 1
            per_page = 10

            while notice_count < per_page:
                try:
                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    print(title)
                    category = try_or_default(lambda: page.locator(xpaths["category"].format(i)).inner_text(timeout=1000), "없음")
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    views = get_views(page, xpaths, i)
                    link = urljoin(base_url, page.locator(xpaths["link"].format(i)).get_attribute("href"))

                    clean_notice_fields(department, major, title, date, views)

                    hash = generate_hash(type, department, major, title, uploader)

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
                        "isPinned": False
                    }
                    notice_count += 1
                    i += 1

                except Exception as e:
                    print(f"[{type} - {department} - {major}] 일반공지 {i}번 에러: {e}")
                    browser.close()
                    return

        browser.close()



# title = "AI캡스톤프로젝트 교과목 WE-Meet 프로젝트 수업 수강신청 안내"

# found = [k for k in keywords_list if k in title]

# if found:
#     send_notice(found, title)
# else:
#     print("포함된 키워드 없음")



# 단과대 공지 데이터 설정
get_notice("단과대", "공과대학", None, 2)
print("공과대학", "크롤링 완료")