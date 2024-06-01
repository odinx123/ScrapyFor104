# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import re

class Scrapyfor104Pipeline:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('SQL_HOST'),
            user=crawler.settings.get('SQL_USER'),
            password=crawler.settings.get('SQL_PASSWORD'),
            database=crawler.settings.get('SQL_JOB104DATABASE'),
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
    
    def convert_salary_to_range(self, salary):  # return 月薪範圍 [min, max] type=tuple
        # 轉換各種薪資格式為月薪範圍 [min, max]
        if '待遇面議' in salary:
            return (0, 1.7976931348623157E+308)  # 表示全符合
        
        salary = salary.replace(',', '')  # 去除千分位符號

        if '月薪' in salary:
            if '以上' in salary:
                min_salary = int(re.findall(r'\d+', salary)[0])
                return (min_salary, 1.7976931348623157E+308)
            else:
                salary = tuple(re.findall(r'\d+', salary))
                return salary
        elif '年薪' in salary:
            s = tuple(map(int, re.findall(r'\d+', salary)))
            if '以上' in salary:
                return (s[0] // 12, 1.7976931348623157E+308)
            if len(s) == 1:
                return (s[0] // 12,)
            else:
                return (s[0]//12, s[1]//12)
        elif '時薪' in salary:
            s = tuple(map(int, re.findall(r'\d+', salary)))
            if '以上' in salary:
                return (s[0] * 8 * 5 * 4, 1.7976931348623157E+308)
            if len(s) == 1:
                return (s[0] * 8 * 5 * 4,)
            else:
                return (s[0] * 8 * 5 * 4, s[1] * 8 * 5 * 4)

        return (0, 0)

    def process_item(self, item, spider):
        try:
            # get the item data
            job_title = item['job_title']
            company = item['company']
            address = item['address']
            industry = item['industry']
            update_time = item['update_time']
            salary_min, salary_max = self.convert_salary_to_range(item['salary'])

            self.cursor.execute(f'''
                                INSERT IGNORE INTO `job`
                                (`job_title`, `company`, `salary_min`, `salary_max`, `address`, `industry`, `update_time`)
                                VALUES
                                ('{job_title}', '{company}', '{salary_min}', '{salary_max}', '{address}', '{industry}', '{update_time}')
                                '''
            )

            edu = [e for e in item['edu'] if '以上' not in e]
            for e in edu:
                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Education`
                                    (`level`)
                                    VALUES
                                    ('{e}')
                                    '''
                )

            exp = item['exp']
            self.cursor.execute(f'''
                                INSERT IGNORE INTO `Experience`
                                (`experience`)
                                VALUES
                                ('{exp}')
                                '''
            )

            skill = item['skill']
            for s in skill:
                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Skills`
                                    (`name`)
                                    VALUES
                                    ('{s}')
                                    '''
                )

            category_name = item['category_name']
            for c in category_name:
                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Categories`
                                    (`category_name`)
                                    VALUES
                                    ('{c}')
                                    '''
                )

            specialty_tool = item['specialty_tool']
            for t in specialty_tool:
                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Tools`
                                    (`specialty_tool`)
                                    VALUES
                                    ('{t}')
                                    '''
                )

            # insert Job_Category with job_id and Job_Category
            self.cursor.execute(f'''
                                SELECT `job_id` FROM `job` WHERE `job_title` = '{job_title}' AND `company` = '{company}'
                                '''
            )
            job_id = self.cursor.fetchone()[0]  # get current job_id

            for c in category_name:
                self.cursor.execute(f'''
                                    SELECT `category_id` FROM `Categories` WHERE `category_name` = '{c}'
                                    '''
                )
                category_id = self.cursor.fetchone()[0]

                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Job_Category`
                                    (`job_id`, `category_id`)
                                    VALUES
                                    ('{job_id}', '{category_id}')
                                    '''
                )

            # insert Job_Tool with job_id and tool_id
            for t in specialty_tool:
                self.cursor.execute(f'''
                                    SELECT `tool_id` FROM `Tools` WHERE `specialty_tool` = '{t}'
                                    '''
                )
                tool_id = self.cursor.fetchone()[0]

                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Job_Tool`
                                    (`job_id`, `tool_id`)
                                    VALUES
                                    ('{job_id}', '{tool_id}')
                                    '''
                )
            
            # insert Job_Skill with job_id and skill_id
            for s in skill:
                self.cursor.execute(f'''
                                    SELECT `skill_id` FROM `Skills` WHERE `name` = '{s}'
                                    '''
                )
                skill_id = self.cursor.fetchone()[0]

                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Job_Skill`
                                    (`job_id`, `skill_id`)
                                    VALUES
                                    ('{job_id}', '{skill_id}')
                                    '''
                )

            # insert Job_Education with job_id and education_id
            for e in edu:
                self.cursor.execute(f'''
                                    SELECT `education_id` FROM `Education` WHERE `level` = '{e}'
                                    '''
                )
                education_id = self.cursor.fetchone()[0]

                self.cursor.execute(f'''
                                    INSERT IGNORE INTO `Job_Education`
                                    (`job_id`, `education_id`)
                                    VALUES
                                    ('{job_id}', '{education_id}')
                                    '''
                )

            # insert Job_Experience with job_id and experience_id
            self.cursor.execute(f'''
                                SELECT `experience_id` FROM `Experience` WHERE `experience` = '{exp}'
                                '''
            )
            experience_id = self.cursor.fetchone()[0]

            self.cursor.execute(f'''
                                INSERT IGNORE INTO `Job_Experience`
                                (`job_id`, `experience_id`)
                                VALUES
                                ('{job_id}', '{experience_id}')
                                '''
            )

            self.connection.commit()

            return item
        except:
            raise DropItem('Insert data failed')
