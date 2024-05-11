import mysql.connector
import pprint

connection = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='9879',
                                     )


# 表示開始使用
cursor = connection.cursor()

# 執行指令
cursor.execute('USE `job104`')

# cursor.execute('delete from job')
# connection.commit()

# 顯示所有資料庫
cursor.execute('select * from `job` order by `update_time`')
records = cursor.fetchall()

pprint.pp(records)


# 結束使用
cursor.close()
# 關閉連線
connection.close()