from queryData.jobQuery import JobDatabase
from app_config import APP_DATABASE, CRAWL_DATABASE, db_config
import os

def main():
    job104_db = JobDatabase(**db_config(CRAWL_DATABASE))

    job104_db.remove_all_table_data()

    # crawl data to job104 database
    os.chdir('./scrapyFor104')
    os.system('scrapy crawl crawlJob104')
    os.chdir('..')
    ###############################

    jobDatabase_db = JobDatabase(**db_config(APP_DATABASE))

    jobDatabase_db.move_data_from(CRAWL_DATABASE)

if __name__ == '__main__':
    main()
