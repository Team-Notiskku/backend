BASE_URL = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
XPATH = {
    "category": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/span[1]',
    "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
    "id": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[1]',
    "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
    "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
    "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
    "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
}