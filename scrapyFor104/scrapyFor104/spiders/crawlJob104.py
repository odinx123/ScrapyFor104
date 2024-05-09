from scrapy_selenium import SeleniumRequest
from scrapyFor104.items import Scrapyfor104Item
from bs4 import BeautifulSoup
import scrapy
import re


class Crawljob104Spider(scrapy.Spider):
    name = "crawlJob104"
    head = {
            'content-type': 'text/html; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.104.com.tw/jobs/search/'
        }

    def start_requests(self):
        # https://static.104.com.tw/category-tool/json/Area.json    地址網址
        # https://static.104.com.tw/category-tool/json/JobCat.json  職務類別
        url = f"http://static.104.com.tw/category-tool/json/JobCat.json"

        yield scrapy.Request(url=url,  # 先將所有職務類別抓入
                             headers=self.head,
                             callback=self.parse
                            )

    def parse(self, response):  # HtmlResponse
        html_text = response.body.decode('utf-8')
        no_list = re.findall(r'"no":"(\d{10})"', html_text)
        
        page_size = 1
        for no in no_list:
            for page in range(1, page_size+1):
                url = f'https://www.104.com.tw/jobs/search/?jobcat={no}&page={page}'
                yield SeleniumRequest(url=url,
                                      headers=self.head,
                                      callback=self.parseEveryPage,
                                     )

    def parseEveryPage(self, response):
        item = Scrapyfor104Item()

        soup = BeautifulSoup(response.body, 'html.parser')
        target_items = soup.select('.b-block--top-bord.job-list-item.b-clearfix.js-job-item:not(.js-job-item--recommend)')

        item['Job_Category'] = re.search(r'「(.*?)」', response.body.decode('utf-8')).group(1)
        for job in target_items:
            item['name'] = job['data-job-name']
            # [address, exp, edu]
            temp = job.find('ul', class_='b-list-inline b-clearfix job-list-intro b-content').find_all('li')
            item['address'] = temp[0].text
            item['exp'] = temp[1].text
            item['edu'] = temp[2].text
            item['update_time'] = job.find(class_='b-tit__date').text.strip()
            item['salary'] = job.find(class_='b-tag--default').text

        yield item
