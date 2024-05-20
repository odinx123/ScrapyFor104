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
# ALTER TABLE my_table ADD PRIMARY KEY (id, name);
# 創建臨時表來保存需要刪除的名稱
# cursor.execute('CREATE TEMPORARY TABLE temp_names SELECT `name` FROM `job`')
# # 刪除 job 表中名稱在臨時表中的記錄
# cursor.execute('DELETE FROM `job` WHERE `name` IN (SELECT `name` FROM `temp_names`)')
# # 刪除臨時表
# cursor.execute('DROP TEMPORARY TABLE temp_names')
# cursor.execute('ALTER TABLE `job` ADD PRIMARY KEY (`name`, `job_category`)')
# cursor.execute('DELETE FROM `job`')
# cursor.execute('ALTER TABLE `job` ADD COLUMN `company` varchar(20)')
# cursor.execute('DROP TABLE job')
# cursor.execute('DESCRIBE `job`')
# cursor.execute('show tables')
# cursor.execute('select `name`, `company` FROM `job`')
# records = cursor.fetchall()
# # print(records)

# exist = set()
# for t in records:
#     if t in exist:
#         print(t)
#     else:
#         exist.add(t)
# print('===================================')
# print(len(records), len(exist))

query = '''
                    SELECT * FROM job
                    WHERE job_id IN (
                        SELECT job_id FROM Job_Tool
                        WHERE tool_id IN (
                            SELECT tool_id FROM Tools
                            WHERE specialty_tool = %s
                        )
                    )
                '''
cursor.execute(query, ('C++',))
jobs = cursor.fetchall()
print(jobs)


# connection.commit()


# 結束使用
cursor.close()
# 關閉連線
connection.close()