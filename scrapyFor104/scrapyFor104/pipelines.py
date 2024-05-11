# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import mysql.connector
import opencc

class Scrapyfor104Pipeline:
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SQL_HOST'),
            user=crawler.settings.get('SQL_USER'),
            password=crawler.settings.get('SQL_PASSWORD'),
            database=crawler.settings.get('SQL_JOB104DATABASE'),
            table=crawler.settings.get('SQL_JOB104TABLE')
        )

    def open_spider(self, spider):
        print(self.host, self.user, self.password)
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # 表示開始使用
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # 結束使用
        self.cursor.close()
        # 關閉連線
        self.connection.close()
    
    def process_item(self, item, spider):
        try:
            # print('=======================================')
            name = item['name']
            salary = item['salary']
            job_category = item['job_category']
            update_time = datetime.strptime(item['update_time'], "%m/%d").replace(year=datetime.now().year).strftime("%Y/%m/%d")
            exp = item['exp']
            address = item['address']
            edu = item['edu']
            # print(name, salary, job_category, update_time, exp, address, edu)
            self.cursor.execute(f'''
                                INSERT INTO `{self.table}`
                                (`name`, `salary`, `job_category`, `update_time`, `exp`, `address`, `edu`)
                                VALUES
                                ('{name}', '{salary}', '{job_category}', '{update_time}', '{exp}', '{address}', '{edu}')
                                '''
            )

            self.connection.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'Error inserting item: {e}')

class StockInfoPipeline:
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.converter = opencc.OpenCC('s2t.json')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SQL_HOST'),
            user=crawler.settings.get('SQL_USER'),
            password=crawler.settings.get('SQL_PASSWORD'),
            database=crawler.settings.get('SQL_DATABASE'),
            table=crawler.settings.get('SQL_TABLE')
        )

    def open_spider(self, spider):
        print(self.host, self.user, self.password)
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # 表示開始使用
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # 結束使用
        self.cursor.close()
        # 關閉連線
        self.connection.close()
    
    def process_item(self, item, spider):
        try:
            # print('=======================================')
            title = self.converter.convert(item['title'])
            url = self.converter.convert(item['url'])
            content = self.converter.convert(item['content'])
            self.cursor.execute(f'''
                                INSERT INTO `{self.table}`
                                (`title`, `url`, `content`)
                                VALUES
                                ('{title}', '{url}', '{content}')
                                '''
            )

            self.connection.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'Error inserting item: {e}')
        # except:
        #     raise DropItem(f'item have nothing.')
