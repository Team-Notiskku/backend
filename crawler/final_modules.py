from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from google.cloud import firestore
import re
import hashlib

def generate_hash(type, department, major, title, uploader):
    key = f"{type.strip()}|{(department or '').strip()}|{(major or '').strip()}|{title.strip()}|{(uploader or '').strip()}"
    return hashlib.md5(key.encode()).hexdigest()