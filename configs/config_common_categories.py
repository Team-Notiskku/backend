CATEGORY_BASE_URLS = {
    "학사" : "https://www.skku.edu/skku/campus/skk_comm/notice02.do",
    "입학" : "https://www.skku.edu/skku/campus/skk_comm/notice03.do",
    "취업" : "https://www.skku.edu/skku/campus/skk_comm/notice04.do",
    "채용/모집" : "https://www.skku.edu/skku/campus/skk_comm/notice05.do",
    "장학" : "https://www.skku.edu/skku/campus/skk_comm/notice06.do",
    "행사/세미나" : "https://www.skku.edu/skku/campus/skk_comm/notice07.do",
    "일반" : "https://www.skku.edu/skku/campus/skk_comm/notice08.do"
}
CATEGORY_XPATH = {
    "category": '',
    "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
    "id": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[1]',
    "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
    "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
    "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
    "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
}