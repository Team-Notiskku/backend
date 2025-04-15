from crawler.modules import get_base_url
import pytest

def test_전체공지_base_url():
    base_url = get_base_url("전체", None, None)
    expected_base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
    assert base_url == expected_base_url

def test_단과대_base_url():
    base_url = get_base_url("단과대", "생명공학대학", None)
    expected_base_url = "https://biotech.skku.edu/biotech/community/under_notice.do"
    assert base_url == expected_base_url

def test_학과_base_url():
    base_url = get_base_url("학과", None, "바이오메카트로닉스학과")
    expected_base_url = "https://skb.skku.edu/biomecha/community/notice.do"
    assert base_url == expected_base_url

def test_잘못된_base_url():
    base_url = get_base_url("단과대", "소프트웨어융합대학", None)
    expected_base_url = "https://biotech.skku.edu/biotech/community/under_notice.do"
    assert base_url != expected_base_url

def test_알_수_없는_공지_예외():
    with pytest.raises(ValueError) as exc_info:
        get_base_url("기타", "경영대학", "경영학과")
    
    assert "알 수 없는 공지" in str(exc_info.value)