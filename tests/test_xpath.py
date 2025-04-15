from crawler.final_modules import get_xpath
import pytest

def test_전체공지_xpath():
    xpath = get_xpath("전체", None, None)
    expected_xpath = {
        "category": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
    }
    assert xpath == expected_xpath

def test_단과대_예외_xpath():
    xpath = get_xpath("단과대", "소프트웨어융합대학", None)
    expected_xpath = {
        "category": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/span',
        "title": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a'
    }
    assert xpath == expected_xpath

def test_학과_예외_xpath():
    xpath = get_xpath("학과", None, "전자전기공학부")
    expected_xpath = {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '',
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    }
    assert xpath == expected_xpath

def test_알_수_없는_공지_예외():
    with pytest.raises(ValueError) as exc_info:
        get_xpath("기타", "경영대학", "경영학과")
    
    assert "알 수 없는 공지" in str(exc_info.value)