init:
	PYTHONPATH=. python crawler/initialize.py

update:
	PYTHONPATH=. python crawler/actions_department_notice.py

set:
	PYTHONPATH=. python setter/keyword_setter.py
	
## 테스트코드
test:	#전체 테스트
	PYTHONPATH=. pytest -v

test_hash:
	PYTHONPATH=. pytest tests/test_hash.py -v

test_xpath:
	PYTHONPATH=. pytest tests/test_xpath.py -v

test_base_url:
	PYTHONPATH=. pytest tests/test_base_url.py -v

#common:
# 	PYTHONPATH=. python crawler/crawler_common.py

test_dept:
	PYTHONPATH=. python3 crawler/test_modules.py -v