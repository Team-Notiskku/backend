from crawler.modules import get_notice
from configs.config_department import DEPT_URLS

# 단과대 공지 데이터 설정
for department in DEPT_URLS.keys():
    if department == "의과대학":
        print("의과대학은 NET 이슈로 생략합니다")
        continue
    get_notice("단과대", department, None, 2)
    print(department, "크롤링 완료")