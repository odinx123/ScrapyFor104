from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import requests
import pprint
import re

# chrome_options = ChromeOptions()
# # 使用無介面瀏覽模式！！
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--window-size=1024x768')
# # 使用無痕模式
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--lang=en_US.UTF-8')

# with Chrome(options=chrome_options) as driver:
#     #your code inside this indent
#     # https://static.104.com.tw/category-tool/json/Area.json地址網址
#     # https://static.104.com.tw/category-tool/json/JobCat.json職務類別
#     url ='https://www.104.com.tw/job/7uttg?jobsource=hotjob_chr'
#     driver.get(url)

#     time.sleep(1)
# #app > div > div > div.job-header > div.position-fixed.job-header__fixed.w-100.bg-white.job-header__cont > div > div > div.job-header__title
#     new_element_locator = (By.CSS_SELECTOR,
#                            '.ml-3.t4.text-gray-darker > span')
#     element = driver.find_element(*new_element_locator)
    
#     print(element.get_attribute('title')[:-2])
def getHTMLText(url, head=None):
    proxies = {'http':'http://localhost','https':'http://localhost'}
    r = requests.get(url, headers=head, proxies=proxies)
    return r.text

if __name__ == '__main__':
    cafile = 'D:\SoftWare\Anaconda\envs\scrapyFor104\Lib\site-packages\certifi\cacert.pem' # http://curl.haxx.se/ca/cacert.pem
    head = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                'Referer': 'https://www.104.com.tw/'
            }
    html = requests.get('http://static.104.com.tw/category-tool/json/JobCat.json')


    response = re.findall(r'"no":"(\d{10})"', html.text)

    pprint.pp(type(response[0]))