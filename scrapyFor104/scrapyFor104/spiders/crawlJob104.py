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
        # 讀取本地的JSON文件
        with open('category.json', 'r', encoding='utf-8') as file:
            job_cat_data = json.load(file)

        no_list = self.extract_job_cat_nos(job_cat_data)

        start_page = 1
        end_page = 1
        for no in no_list:
            if no[0:4] != '2007': continue  # 只抓取資訊軟體相關職缺
            
            for page in range(start_page, end_page + 1):
                url = f'https://www.104.com.tw/jobs/search/?jobcat={no}&page={page}'
                yield scrapy.Request(url=url,
                                     headers=self.head,
                                     callback=self.parse,
                                    )

    def extract_job_cat_nos(self, data):
        no_list = []
        if isinstance(data, dict):
            if 'n' in data:
                for item in data['n']:
                    no_list.extend(self.extract_job_cat_nos(item))
            elif 'no' in data:  # 有n就不要no(不要大類別的no)
                no_list.append(data['no'])
        elif isinstance(data, list):
            for item in data:
                no_list.extend(self.extract_job_cat_nos(item))
        return no_list

    def parse(self, response):
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
