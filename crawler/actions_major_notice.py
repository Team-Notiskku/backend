from crawler.modules import get_notice
from configs.config_major import MAJOR_URLS

# 학과 공지 데이터 설정
for major in MAJOR_URLS.keys():
    get_notice("학과", None, major, 2)
    print(major, "크롤링 완료")