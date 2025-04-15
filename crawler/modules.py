from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import re

def get_general(base_url, xpaths):
    max_pages = 10 
    notices = [] 

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
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    id = id[3:]
                    if int(id) == latest_id:
                        browser.close()
                        notices.reverse()
                        if latest_id == -1:
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices 
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"

                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    if xpaths["views"] != "" :
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    else:
                        views = 'null'
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")

                    link = urljoin(base_url, link)

                    notices.append([int(id), category, title, date, uploader, views, link])

                except Exception as e:
                    print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                    browser.close()
                    notices.reverse()
                    if latest_id == -1:
                        notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                    return notices

        browser.close()
        notices.reverse()
        if latest_id == -1:
            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

    return notices

def get_pinned(base_url, xpaths, latest_id, is_arch):
    max_pages = 10 
    
    notices = []  
 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            page.goto(full_url)
            page.wait_for_load_state("load")
            if is_arch == 1:
                pinned_notices = page.locator('//*[@id="item_body"]/div[2]/div[1]/div/div[2]/div/div/div/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
            else:
                pinned_notices = page.locator('//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
            pinned_count = pinned_notices.count()  # 고정 공지 개수

            notice_count = 0
            i = pinned_count + 1  # 고정 공지 이후부터 시작

            while notice_count < 10:
                try:
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    id = id[3:]
                    if int(id) == latest_id:
                        browser.close()
                        notices.reverse()
                        if latest_id == -1:
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices 
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"

                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    if xpaths["views"] != "":
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    else:
                        views = 'null'
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")

                    link = urljoin(base_url, link)

                    notices.append([int(id), category, title, date, uploader, views, link])

                    notice_count += 1 
                    i += 1

                except Exception as e:
                    print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                    browser.close()
                    notices.reverse()
                    if latest_id == -1:
                        notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                    return notices

        browser.close()
        notices.reverse()
        if latest_id == -1:
            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

    return notices

def get_exceptions(SHEET_NAME, base_url, xpaths, latest_id):
    if SHEET_NAME == "화학과":
        max_pages = 10 
        notices = []

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
                        id = 0
                        category = "없음"
                        title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                        date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                        date = date[14:]
                        if date == latest_id:
                            browser.close()
                            notices.reverse()
                            if latest_id == -1:
                                notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                            return notices 
                        uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                        uploader = uploader[9:]
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                        views = views[6:]
                        link = page.locator(xpaths["link"].format(i)).get_attribute("href")
                         
                        link = urljoin(base_url, link)

                        notices.append([int(id), category, title, date, uploader, views, link])

                    except Exception as e:
                        print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                        browser.close()
                        notices.reverse()
                        if latest_id == -1: # initializer일때
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices

            browser.close()
            notices.reverse()
            if latest_id == -1: # initializer일때
                notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

        return notices
    elif SHEET_NAME == "약학대학":
        max_pages = 10 
    
        notices = [] # updater일떄

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_num in range(max_pages):
                cur_page = page_num+1
                full_url = f"{base_url}&page={cur_page}#subcon"
                
                page.goto(full_url)
                page.wait_for_load_state("load")
                for i in range(1, 11):
                    try:
                        category = "없음"
                        title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                        date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                        uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                        views = 'null'
                        link = page.locator(xpaths["link"].format(i)).get_attribute("href")
                        match = re.match(r"^\d+", title)
                        if match:
                            id = match.group()
                            title = title[5:]
                        else:
                            id = 0
                        if int(id) == latest_id:
                            browser.close()
                            notices.reverse()
                            if latest_id == -1: # initializer일때
                                notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                            return notices 
                        link = urljoin(base_url, link)

                        notices.append([int(id), category, title, date, uploader, views, link])

                    except Exception as e:
                        print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                        browser.close()
                        notices.reverse()
                        if latest_id == -1:
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices

            browser.close()
            notices.reverse()
            if latest_id == -1: # initializer일때
                notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

        return notices
    elif SHEET_NAME == "의과대학":
        max_pages = 10 
    
        if latest_id == -1: # initializer일때
            notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]
        else:
            notices = [] # updater일떄

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_num in range(max_pages):
                cur_page = page_num+1
                notice_url = f"?keyword=&startpage=1&bcode=nt&pg={cur_page}"
                full_url = urljoin(base_url, notice_url)
                
                page.goto(full_url)
                page.wait_for_load_state("load")

                for i in range(1, 11):
                    try:
                        id = page.locator(xpaths["id"].format(i)).evaluate("el => el.innerText + window.getComputedStyle(el, '::after').content")
                        id = id.split(".")[-1].strip(' []"')
                        if int(id) == latest_id:
                            browser.close()
                            notices[1:] = sorted(notices[1:], key=lambda x: x[0])  
                            return notices 
                        category = "없음"

                        title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                        date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                        uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                        views = views[4:]

                        link = page.locator(xpaths["link"].format(i)).get_attribute("href")

                        link = urljoin(base_url, link)

                        notices.append([int(id), category, title, date, uploader, views, link])

                    except Exception as e:
                        print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                        browser.close()
                        notices.reverse()
                        if latest_id == -1:
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices

        browser.close()
        notices.reverse()
        if latest_id == -1:
            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

        return notices
    else:
        return []