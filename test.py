from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

chrome_options = ChromeOptions()
# 使用無介面瀏覽模式！！
chrome_options.add_argument('--headless')
# 使用無痕模式
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--lang=en_US.UTF-8')

with Chrome(options=chrome_options) as driver:
    #your code inside this indent
    url ='https://baike.baidu.com/wikitag/taglist?tagId=62991'
    driver.get(url)

    driver.maximize_window()
    time.sleep(2)

    
    new_element_locator = (By.CLASS_NAME, 'waterFall_item')
    elements = driver.find_elements(*new_element_locator)
    
    page_size = 3
    for i in range(page_size):
        # 滾動到頁面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        num_loaded_elements = len(elements)
        WebDriverWait(driver, 10).until(
            lambda driver: len(driver.find_elements(*new_element_locator)) > num_loaded_elements
        )
        elements = driver.find_elements(*new_element_locator)


    print('長度', len(elements))