from queryData.jobAPI import JobDatabase
import os

def main():
    SQL_USER = os.environ["USER_NAME"]
    SQL_HOST = os.environ["HOST"]
    SQL_PASSWORD = os.environ["PASSWD"]

    job104_db = JobDatabase(
        host=SQL_HOST,
        username=SQL_USER,
        password=SQL_PASSWORD,
        database="job104"
    )

    # job104_db = JobDatabase(
    #     host="localhost",
    #     username="root",
    #     password="9879",
    #     database="job104"
    # )

    job104_db.remove_all_table_data()

    # crawl data to job104 database
    os.chdir('./scrapyFor104')
    os.system('scrapy crawl crawlJob104')
    os.chdir('..')
    ###############################

    jobDatabase_db = JobDatabase(
        host=SQL_HOST,
        username=SQL_USER,
        password=SQL_PASSWORD,
        database="jobDatabase"
    )

    # jobDatabase_db = JobDatabase(
    #     host="localhost",
    #     username="root",
    #     password="9879",
    #     database="jobDatabase"
    # )

    jobDatabase_db.move_data_from("job104")

if __name__ == '__main__':
    main()