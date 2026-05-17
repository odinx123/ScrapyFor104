import hashlib
import re
import unicodedata

import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


MAX_MYSQL_FLOAT = 3.40282e38


class Scrapyfor104Pipeline:
    def __init__(self, host, port, user, password, database, batch_size):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.batch_size = max(1, int(batch_size or 1))
        self.buffer = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("SQL_HOST"),
            port=crawler.settings.getint("SQL_PORT"),
            user=crawler.settings.get("SQL_USER"),
            password=crawler.settings.get("SQL_PASSWORD"),
            database=crawler.settings.get("SQL_JOB104DATABASE"),
            batch_size=crawler.settings.getint("MYSQL_PIPELINE_BATCH_SIZE", 100),
        )

    def open_spider(self, spider=None):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        self.ensure_job_dedupe_schema()
        if spider:
            spider.logger.info(
                "Opened MySQL pipeline for %s:%s/%s with batch size %s",
                self.host,
                self.port,
                self.database,
                self.batch_size,
            )

    def close_spider(self, spider=None):
        self.flush(spider)
        self.cursor.close()
        self.connection.close()

    def convert_salary_to_range(self, salary):
        salary = str(salary or "").replace(",", "")
        if "待遇面議" in salary:
            return 0, MAX_MYSQL_FLOAT

        numbers = [int(value) for value in re.findall(r"\d+", salary)]
        if not numbers:
            return 0, 0

        if "年薪" in salary:
            numbers = [value // 12 for value in numbers]
        elif "時薪" in salary:
            numbers = [value * 8 * 5 * 4 for value in numbers]

        if "以上" in salary:
            return numbers[0], MAX_MYSQL_FLOAT
        if len(numbers) == 1:
            return numbers[0], numbers[0]
        return numbers[0], numbers[1]

    def process_item(self, item, spider=None):
        try:
            self.buffer.append(self.normalize_item(item))
            if len(self.buffer) >= self.batch_size:
                self.flush(spider)
            return item
        except DropItem:
            raise
        except Exception as exc:
            raise DropItem(f"Insert data failed: {exc}") from exc

    def normalize_item(self, item):
        adapter = ItemAdapter(item)
        salary_min, salary_max = self.convert_salary_to_range(adapter.get("salary"))
        education = [value for value in self.as_list(adapter.get("edu")) if "以上" not in value]
        job_title = adapter.get("job_title")
        company = adapter.get("company")
        address = adapter.get("address")

        return {
            "source_job_key": adapter.get("source_job_key"),
            "source_url": adapter.get("source_url"),
            "dedupe_key": self.build_dedupe_key(job_title, company, address),
            "job_title": job_title,
            "company": company,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "address": address,
            "industry": adapter.get("industry"),
            "update_time": adapter.get("update_time"),
            "education": education,
            "experience": adapter.get("exp"),
            "skills": self.as_list(adapter.get("skill")),
            "categories": self.as_list(adapter.get("category_name")),
            "tools": self.as_list(adapter.get("specialty_tool")),
        }

    def build_dedupe_key(self, job_title, company, address):
        normalized = "|".join(
            [
                self.normalize_text(company),
                self.normalize_text(job_title),
                self.normalize_text(address),
            ]
        )
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest()

    def normalize_text(self, value):
        value = unicodedata.normalize("NFKC", str(value or ""))
        value = re.sub(r"\s+", "", value)
        return value.casefold()

    def as_list(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return [item for item in value if item]
        if isinstance(value, (tuple, set)):
            return [item for item in value if item]
        return [value]

    def flush(self, spider=None):
        if not self.buffer:
            return

        batch = self.buffer
        try:
            self.insert_jobs(batch)
            education_ids = self.insert_dimension("Education", "education_id", "level", self.collect(batch, "education"))
            experience_ids = self.insert_dimension("Experience", "experience_id", "experience", self.collect_one(batch, "experience"))
            skill_ids = self.insert_dimension("Skills", "skill_id", "name", self.collect(batch, "skills"))
            category_ids = self.insert_dimension("Categories", "category_id", "category_name", self.collect(batch, "categories"))
            tool_ids = self.insert_dimension("Tools", "tool_id", "specialty_tool", self.collect(batch, "tools"))

            job_ids = self.fetch_job_ids(batch)
            self.clear_job_links(job_ids.values())

            self.insert_links("Job_Education", "education_id", batch, job_ids, education_ids, "education")
            self.insert_links("Job_Skill", "skill_id", batch, job_ids, skill_ids, "skills")
            self.insert_links("Job_Category", "category_id", batch, job_ids, category_ids, "categories")
            self.insert_links("Job_Tool", "tool_id", batch, job_ids, tool_ids, "tools")
            self.insert_experience_links(batch, job_ids, experience_ids)

            self.connection.commit()
            if spider:
                spider.logger.info("Flushed %s scraped jobs to MySQL", len(batch))
            self.buffer = []
        except mysql.connector.Error as exc:
            self.connection.rollback()
            raise DropItem(f"Insert batch failed: {exc}") from exc

    def insert_jobs(self, batch):
        rows = [
            (
                item["source_job_key"],
                item["source_url"],
                item["dedupe_key"],
                item["job_title"],
                item["company"],
                item["salary_min"],
                item["salary_max"],
                item["address"],
                item["industry"],
                item["update_time"],
            )
            for item in batch
        ]
        self.cursor.executemany(
            """
            INSERT INTO `job`
            (`source_job_key`, `source_url`, `dedupe_key`, `job_title`, `company`,
             `salary_min`, `salary_max`, `address`, `industry`, `update_time`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                `source_job_key` = COALESCE(VALUES(`source_job_key`), `source_job_key`),
                `source_url` = COALESCE(VALUES(`source_url`), `source_url`),
                `dedupe_key` = COALESCE(`dedupe_key`, VALUES(`dedupe_key`)),
                `job_title` = VALUES(`job_title`),
                `company` = VALUES(`company`),
                `salary_min` = VALUES(`salary_min`),
                `salary_max` = VALUES(`salary_max`),
                `address` = VALUES(`address`),
                `industry` = VALUES(`industry`),
                `update_time` = VALUES(`update_time`)
            """,
            rows,
        )

    def insert_dimension(self, table, id_column, value_column, values):
        values = sorted({value for value in values if value})
        if not values:
            return {}

        self.cursor.executemany(
            f"INSERT IGNORE INTO `{table}` (`{value_column}`) VALUES (%s)",
            [(value,) for value in values],
        )

        placeholders = ", ".join(["%s"] * len(values))
        self.cursor.execute(
            f"SELECT `{id_column}`, `{value_column}` FROM `{table}` WHERE `{value_column}` IN ({placeholders})",
            tuple(values),
        )
        return {value: row_id for row_id, value in self.cursor.fetchall()}

    def fetch_job_ids(self, batch):
        keys = sorted({item["dedupe_key"] for item in batch if item["dedupe_key"]})
        if not keys:
            return {}

        placeholders = ", ".join(["%s"] * len(keys))
        self.cursor.execute(
            f"SELECT `job_id`, `dedupe_key` FROM `job` WHERE `dedupe_key` IN ({placeholders})",
            tuple(keys),
        )
        return {dedupe_key: job_id for job_id, dedupe_key in self.cursor.fetchall()}

    def clear_job_links(self, job_ids):
        job_ids = sorted({job_id for job_id in job_ids if job_id})
        if not job_ids:
            return

        placeholders = ", ".join(["%s"] * len(job_ids))
        for table in ("Job_Education", "Job_Skill", "Job_Category", "Job_Tool", "Job_Experience"):
            self.cursor.execute(
                f"DELETE FROM `{table}` WHERE `job_id` IN ({placeholders})",
                tuple(job_ids),
            )

    def insert_links(self, table, target_column, batch, job_ids, target_ids, source_field):
        rows = set()
        for item in batch:
            job_id = job_ids.get(item["dedupe_key"])
            if not job_id:
                continue
            for value in item[source_field]:
                target_id = target_ids.get(value)
                if target_id:
                    rows.add((job_id, target_id))

        if rows:
            self.cursor.executemany(
                f"INSERT IGNORE INTO `{table}` (`job_id`, `{target_column}`) VALUES (%s, %s)",
                sorted(rows),
            )

    def insert_experience_links(self, batch, job_ids, experience_ids):
        rows = set()
        for item in batch:
            job_id = job_ids.get(item["dedupe_key"])
            experience_id = experience_ids.get(item["experience"])
            if job_id and experience_id:
                rows.add((job_id, experience_id))

        if rows:
            self.cursor.executemany(
                "INSERT IGNORE INTO `Job_Experience` (`job_id`, `experience_id`) VALUES (%s, %s)",
                sorted(rows),
            )

    def collect(self, batch, field):
        values = []
        for item in batch:
            values.extend(item[field])
        return values

    def collect_one(self, batch, field):
        return [item[field] for item in batch if item[field]]

    def ensure_job_dedupe_schema(self):
        columns = self.get_job_columns()
        add_columns = []
        if "source_job_key" not in columns:
            add_columns.append("ADD COLUMN `source_job_key` varchar(32) NULL AFTER `job_id`")
        if "source_url" not in columns:
            add_columns.append("ADD COLUMN `source_url` varchar(255) NULL AFTER `source_job_key`")
        if "dedupe_key" not in columns:
            add_columns.append("ADD COLUMN `dedupe_key` char(40) NULL AFTER `source_url`")

        if add_columns:
            self.cursor.execute(f"ALTER TABLE `job` {', '.join(add_columns)}")
            self.connection.commit()

        indexes = self.get_job_indexes()
        if "uq_job_dedupe_key" not in indexes:
            self.cursor.execute("CREATE UNIQUE INDEX `uq_job_dedupe_key` ON `job` (`dedupe_key`)")
        if "uq_job_source_key" not in indexes:
            self.cursor.execute("CREATE UNIQUE INDEX `uq_job_source_key` ON `job` (`source_job_key`)")
        self.connection.commit()

    def get_job_columns(self):
        self.cursor.execute("SHOW COLUMNS FROM `job`")
        return {row[0] for row in self.cursor.fetchall()}

    def get_job_indexes(self):
        self.cursor.execute("SHOW INDEX FROM `job`")
        return {row[2] for row in self.cursor.fetchall()}
