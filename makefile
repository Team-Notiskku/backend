common:
	PYTHONPATH=. python crawler/crawler_common.py

test_hash:
	PYTHONPATH=. pytest tests/test_hash.py -v