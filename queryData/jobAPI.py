import mysql.connector
import re

INF = float('inf')

class JobDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = self.connect_to_database()

    # 建立資料庫連接
    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
            return conn
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)
            return None
    
    # 關閉資料庫連接
    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("MySQL connection closed.")
        else:
            print("No connection to close.")

    # 解構函數：關閉資料庫連接
    def __del__(self):
        self.close_connection()

    # ================================================================= #

    # 獲取所有工作
    def get_jobs(self, num=None):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                if num is None:
                    cursor.execute("SELECT * FROM job")
                else:
                    cursor.execute(f"SELECT * FROM job LIMIT {num}")
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # 獲取表的列名稱
    def get_columns(self, table_name):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [column[0] for column in cursor.fetchall()]
                return columns
            except mysql.connector.Error as e:
                print(f"Error retrieving columns from {table_name}:", e)
        else:
            print("Connection to MySQL not established.")
    
    # 獲取所有表
    def get_all_table(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = []
                for table in cursor.fetchall():
                    tables.append(table[0])
                return tables
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
    
    # 列出所有工作類別
    def get_all_categories(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT category_name FROM Categories")
                categories = [category[0] for category in cursor.fetchall()]
                return categories
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # category 找出所有工作
    def get_jobs_by_category(self, category):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE job_id IN (
                        SELECT job_id FROM Job_Category
                        WHERE category_id IN (
                            SELECT category_id FROM Categories
                            WHERE category_name = %s
                        )
                    )
                '''
                cursor.execute(query, (category,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # 得到所有技能
    def get_all_skills(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT `name` FROM Skills")
                skills = [skill[0] for skill in cursor.fetchall()]
                return skills
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # skill 找出所有工作
    def get_jobs_by_skill(self, skill):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE `job_id` IN (
                        SELECT `job_id` FROM `Job_Skill`
                        WHERE `skill_id` IN (
                            SELECT `skill_id` FROM `Skills`
                            WHERE `name` = %s
                        )
                    )
                '''
                cursor.execute(query, (skill,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # 得到所有experience
    def get_all_experiences(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT experience FROM Experience")
                experiences = [experience[0] for experience in cursor.fetchall()]
                return experiences
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # experience 找出所有工作
    def get_jobs_by_experience(self, experience):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE job_id IN (
                        SELECT job_id FROM Job_Experience
                        WHERE experience_id IN (
                            SELECT experience_id FROM Experience
                            WHERE experience = %s
                        )
                    )
                '''
                cursor.execute(query, (experience,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
        
    # 得到所有education
    def get_all_educations(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT level FROM Education")
                educations = [education[0] for education in cursor.fetchall()]
                return educations
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # education 找出所有工作
    def get_jobs_by_education(self, education):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE job_id IN (
                        SELECT job_id FROM Job_Education
                        WHERE education_id IN (
                            SELECT education_id FROM Education
                            WHERE level = %s
                        )
                    )
                '''
                cursor.execute(query, (education,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
    
    # 得到所有tool
    def get_all_tools(self):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT `specialty_tool` FROM Tools")
                tools = [tool[0] for tool in cursor.fetchall()]
                return tools
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
    
    # tool 找出所有工作
    def get_jobs_by_tool(self, tool):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
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
                cursor.execute(query, (tool,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    def is_within_range(self, salary_range, min_salary, max_salary):
        # 檢查給定範圍是否與薪資範圍重疊
        try:
            if min_salary <= salary_range[0] <= max_salary:
                return True
            elif min_salary <= salary_range[1] <= max_salary:
                return True
        except:
            pass
        return False

    # salary 找出所有工作在 [min_salary - max_salary]之間，不要用convert_salary_to_range
    def get_jobs_by_salary(self, min_salary, max_salary):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                # mysql存的是(min, max)的tuple
                query = '''
                    SELECT * FROM job
                    WHERE salary_min BETWEEN %s AND %s OR salary_max BETWEEN %s AND %s
                '''
                cursor.execute(query, (min_salary, max_salary)*2)
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # 得到所有salary
    def get_all_salaries(self):  # return 月薪範圍 [min, max] type=tuple
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DISTINCT salary_min, salary_max FROM job")
                salaries = cursor.fetchall()
                return salaries
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
    
    # update_time 找出所有工作 傳入天數，回傳最近幾天內的工作 0代表只有今天，1包含昨天
    def get_jobs_by_update_time(self, days):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE `update_time` >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                '''
                cursor.execute(query, (days,))
                jobs = cursor.fetchall()
                return jobs
            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")

    # filter 找出所有工作
    def get_jobs_by_filter(self, category=None, skill=None, experience=None, education=None, tool=None, days=None, min_salary=0, max_salary=INF):
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = '''
                    SELECT * FROM job
                    WHERE 1=1
                '''
                params = []

                if category:
                    if isinstance(category, list):
                        query += '''AND job_id IN (
                                        SELECT job_id FROM Job_Category
                                        WHERE category_id IN (
                                            SELECT category_id FROM Categories
                                            WHERE category_name IN (
                        '''
                        query += ', '.join(['%s']*len(category))
                        query += ')))'
                        params.extend(category)
                    else:
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Category
                                WHERE category_id IN (
                                    SELECT category_id FROM Categories
                                    WHERE category_name = %s
                                )
                            )
                        '''
                        params.append(category)

                if skill:
                    if isinstance(skill, list):
                        query += '''AND job_id IN (
                                        SELECT job_id FROM Job_Skill
                                        WHERE skill_id IN (
                                            SELECT skill_id FROM Skills
                                            WHERE name IN (
                        '''
                        query += ', '.join(['%s']*len(skill))
                        query += ')))'
                        params.extend(skill)
                    else:
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Skill
                                WHERE skill_id IN (
                                    SELECT skill_id FROM Skills
                                    WHERE name = %s
                                )
                            )
                        '''
                        params.append(skill)

                if experience:
                    if isinstance(experience, list):
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Experience
                                WHERE experience_id IN (
                                    SELECT experience_id FROM Experience
                                    WHERE experience IN (
                        '''
                        query += ', '.join(['%s']*len(experience))
                        query += ')))'
                        params.extend(experience)
                    else:
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Experience
                                WHERE experience_id IN (
                                    SELECT experience_id FROM Experience
                                    WHERE experience = %s
                                )
                            )
                        '''
                        params.append(experience)

                if education:
                    if isinstance(education, list):
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Education
                                WHERE education_id IN (
                                    SELECT education_id FROM Education
                                    WHERE level IN (
                        '''
                        query += ', '.join(['%s']*len(education))
                        query += ')))'
                        params.extend(education)
                    else:
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Education
                                WHERE education_id IN (
                                    SELECT education_id FROM Education
                                    WHERE level = %s
                                )
                            )
                        '''
                        params.append(education)

                if tool:
                    if isinstance(tool, list):
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Tool
                                WHERE tool_id IN (
                                    SELECT tool_id FROM Tools
                                    WHERE specialty_tool IN (
                        '''
                        query += ', '.join(['%s']*len(tool))
                        query += ')))'
                        params.extend(tool)
                    else:
                        query += '''
                            AND job_id IN (
                                SELECT job_id FROM Job_Tool
                                WHERE tool_id IN (
                                    SELECT tool_id FROM Tools
                                    WHERE specialty_tool = %s
                                )
                            )
                        '''
                        params.append(tool)
                
                if days is not None:
                    query += ' AND update_time >= DATE_SUB(CURDATE(), INTERVAL %s DAY)'
                    params.append(days)

                if min_salary is not None and max_salary is not None and max_salary >= min_salary:
                    query += 'AND salary_min BETWEEN %s AND %s OR salary_max BETWEEN %s AND %s'
                    params.extend((min_salary, max_salary)*2)

                cursor.execute(query, tuple(params))
                jobs = cursor.fetchall()

                return jobs

            except mysql.connector.Error as e:
                print("Error retrieving data from MySQL:", e)
        else:
            print("Connection to MySQL not established.")
    
def conver_salary_to_PythonStyle(salary_min, salary_max):
    return (salary_min, INF if salary_max == 3.40282e+38 else int(salary_max))

# 測試連接與獲取資料
def main():
    import pprint
    db = JobDatabase(
        host="localhost",
        username="root",
        password="9879",
        database="job104"
    )

    print('=============================================')
    # conver_salary_to_MySQLStyle(INF, INF)
    jobs = db.get_jobs_by_filter(category=['後端工程師', '網路管理工程師'],
                                 skill=None,
                                 experience=None,
                                 education=None,
                                 tool=None,
                                 days=None,
                                 min_salary=None,
                                 max_salary=None
                                )
    try:
        for j in jobs:
            print(j[1], end=',   ')
    except:
        pass

if __name__ == "__main__":
    main()