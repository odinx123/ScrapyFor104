from scrapyFor104.items import Scrapyfor104Item
from bs4 import BeautifulSoup
import scrapy
import re
import json
# import requests

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
        
        page_size = 150
        for i, no in enumerate(no_list):
            if no[-2:] == '00': continue
            if no[0:4] != '2007': continue  # 只抓取資訊軟體相關職缺，因為全部抓太久了
            # if i >= 3: break  # for test
            for page in range(1, page_size+1):
                url = f'https://www.104.com.tw/jobs/search/?jobcat={no}&page={page}'

                yield scrapy.Request(url=url,
                                     headers=self.head,
                                     callback=self.parseEveryPage,
                                    )

    def parseEveryPage(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        if len(soup.select('.b-center.b-txt--center > p[class=b-tit]')) > 0:
            return

        targets =  soup.find_all(attrs={'data-qa-id':'jobSeachResultTitle'})
        
        re_compile = re.compile(r'/job/([^?]+)')
        for tag in targets:
            href = tag['href']
            job_id = re_compile.search(href).group(1)
            
            """取得職缺詳細資料"""
            url = f'https://www.104.com.tw/job/ajax/content/{job_id}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
                'Referer': f'https://www.104.com.tw/job/{job_id}'
            }
            
            yield scrapy.Request(url=url,
                                 headers=headers,
                                 callback=self.parseEveryJob,
                                )
    
    def parseEveryJob(self, response):
        self.log(f'Parsing job details from {response.url}')

        item = Scrapyfor104Item()
        
        job_data = json.loads(response.text)['data']

        header = job_data['header']
        item['job_title'] = header['jobName']
        item['update_time'] = header['appearDate']
        item['company'] = header['custName']

        condition = job_data['condition']

        item['exp'] = condition['workExp']
        item['edu'] = condition['edu'].split('、')

        sk_list = []
        for sk in condition['skill']:
            sk_list.append(sk['description'])
        item['skill'] = sk_list

        tools = []
        for t in condition['specialty']:
            tools.append(t['description'])
        item['specialty_tool'] = tools

        detail = job_data['jobDetail']

        categories = []
        for c in detail['jobCategory']:
            categories.append(c['description'])
        item['category_name'] = categories

        item['salary'] = detail['salary']
        item['address'] = detail['addressRegion'] + detail['addressDetail']

        item['industry'] = job_data['industry']

        yield item
