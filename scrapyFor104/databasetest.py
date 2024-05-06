import pymysql
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem

class MySQLPipeline:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            database=settings['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            cp_reconnect=True,
        )
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self._insert_data, item)
        query.addErrback(self.handle_error)
        return item

    def _insert_data(self, tx, item):
        # 將資料插入到資料庫
        sql = """
        INSERT INTO your_table_name (field1, field2, ..., fieldN)
        VALUES (%s, %s, ..., %s)
        """
        params = (
            item['field1'],
            item['field2'],
            ...,
            item['fieldN']
        )
        tx.execute(sql, params)

    def handle_error(self, failure):
        # 處理異常
        print(failure)
