import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='9879',
                                     )


# 表示開始使用
cursor = connection.cursor()

# 執行指令
cursor.execute('USE testforstockinfo')

# 顯示所有資料庫
cursor.execute('SELECT * FROM stockinfo limit 1')
records = cursor.fetchall()

print(records)

# 結束使用
cursor.close()
# 關閉連線
connection.close()