import hashlib
from crawler.modules import generate_hash 

def test_동일한_공지는_동일한_해시():
    h1 = generate_hash("단과대", "소프트웨어융합대학", "소프트웨어학과", "첫번째 공지사항", "안지운")
    h2 = generate_hash("단과대", "소프트웨어융합대학", "소프트웨어학과", "첫번째 공지사항", "안지운")
    assert h1 == h2  

def test_다른_공지는_다른_해시():
    h1 = generate_hash("단과대", "소프트웨어융합대학", "소프트웨어학과", "첫번째 공지사항", "안지운")
    h2 = generate_hash("단과대", "소프트웨어융합대학", "소프트웨어학과", "두번째 공지사항", "안지운")
    assert h1 != h2 

def test_필드가_없을떄도_해시_생성():
    h = generate_hash("전체공지", None, None, "없는 공지 제목", None)
    expected_key = "전체공지|||없는 공지 제목|"  
    expected_hash = hashlib.md5(expected_key.encode()).hexdigest()
    assert h == expected_hash