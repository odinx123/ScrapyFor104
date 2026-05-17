import os


DB_HOST = os.getenv("SCRAPY104_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("SCRAPY104_DB_PORT", "3306"))
DB_USER = os.getenv("SCRAPY104_DB_USER", "root")
DB_PASSWORD = os.getenv("SCRAPY104_DB_PASSWORD", "9879")
CRAWL_DATABASE = os.getenv("SCRAPY104_CRAWL_DB", "job104")
APP_DATABASE = os.getenv("SCRAPY104_APP_DB", "jobdatabase")


def db_config(database=None):
    return {
        "host": DB_HOST,
        "username": DB_USER,
        "password": DB_PASSWORD,
        "database": database or APP_DATABASE,
        "port": DB_PORT,
    }
