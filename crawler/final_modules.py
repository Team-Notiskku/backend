from playwright.sync_api import sync_playwright
from configs.config_common import XPATH, BASE_URL
from configs.config_department import DEPT_XPATHS, DEPT_URLS
from configs.config_major import MAJOR_XPATHS, MAJOR_URLS
from urllib.parse import urljoin
from google.cloud import firestore
import re
import hashlib

def generate_hash(type, department, major, title, uploader):
    key = f"{type.strip()}|{(department or '').strip()}|{(major or '').strip()}|{title.strip()}|{(uploader or '').strip()}"
    return hashlib.md5(key.encode()).hexdigest()

def get_xpath(type: str, department: str = "", major: str = ""):
    if type == "전체":
        return XPATH 
    elif type == "단과대":
        return DEPT_XPATHS.get(department, {})
    elif type == "학과":
        return MAJOR_XPATHS.get(major, {})  
    else:
        raise ValueError(f"알 수 없는 공지: {type, department, major}")
    
def get_base_url(type: str, department: str = "", major: str = ""):
    if type == "전체":
        return BASE_URL
    elif type == "단과대":
        return DEPT_URLS.get(department, "")
    elif type == "학과":
        return MAJOR_URLS.get(major, "")  
    else:
        raise ValueError(f"알 수 없는 공지: {type, department, major}")