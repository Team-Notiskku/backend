from crawler.modules import get_notice
from configs.config_department import DEPT_URLS
from configs.config_major import MAJOR_URLS

# 전체 공지 데이터 설정
get_notice("전체", None, None, 10)
print("전체 공지 크롤링 완료")

# 단과대 공지 데이터 설정
for department in DEPT_URLS.keys():
    if department == "의과대학":
        print("의과대학은 NET 이슈로 생략합니다")
        continue
    get_notice("단과대", department, None, 10)
    print(department, "크롤링 완료")

# 학과 공지 데이터 설정
for major in MAJOR_URLS.keys():
    get_notice("학과", None, major, 10)
    print(major, "크롤링 완료")