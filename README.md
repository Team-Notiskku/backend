# NotiSKKU Backend

> **노티스꾸**: 성균관대학교 맞춤형 공지사항 알림 애플리케이션   
> 학과별, 키워드별 공지를 받아보고 학사일정을 한눈에 확인하세요!

_본 레포지토리는 NotiSKKU 프로젝트의 크롤링 및 데이터베이스 레포지토리입니다._    
→ [NotiSKKU Repository 바로가기](https://github.com/Team-Notiskku/NotiSKKU)

<img src="assets/readme.png"/>

## 🚀 System Architecture

<img src="assets/Development Architecture - Edited.png"/>

---
## Python Environments
### 1. 가상환경 생성
``` 
python -m venv venv 
```

### 2. 가상환경 활성화
```
source venv/bin/activate
venv\Scripts\activate.bat  #for windows
```
### 3. 패키지 설치
```
pip install -r requirements.txt
```

---

## 📌 Commit Conventions
feat : 새로운 기능 추가  
design : 사용자 UI 변경  
style : 코드 수정 없이 포맷만 변경   
comment : 주석 추가/변경/삭제  
fix : 버그 수정  
refactor : 리팩토링, 개선   
docs : 문서 수정  
rename : 파일/디렉토리명 수정, 이동  
remove : 파일 삭제  
test : 테스트 코드 관련   
chore : 빌드, 패키지 관련 업무   