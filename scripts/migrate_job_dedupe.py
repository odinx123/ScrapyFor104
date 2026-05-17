from collections import defaultdict
from pathlib import Path
import hashlib
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mysql.connector

from app_config import APP_DATABASE, CRAWL_DATABASE, db_config


RELATION_TABLES = (
    ("Job_Education", "education_id"),
    ("Job_Skill", "skill_id"),
    ("Job_Category", "category_id"),
    ("Job_Tool", "tool_id"),
    ("Job_Experience", "experience_id"),
)


def normalize_text(value):
    value = unicodedata.normalize("NFKC", str(value or ""))
    value = re.sub(r"\s+", "", value)
    return value.casefold()


def build_dedupe_key(company, job_title, address):
    normalized = "|".join(
        [
            normalize_text(company),
            normalize_text(job_title),
            normalize_text(address),
        ]
    )
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


def connect(database):
    cfg = db_config(database)
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["username"],
        password=cfg["password"],
        database=cfg["database"],
    )


def ensure_columns(cursor):
    cursor.execute("SHOW COLUMNS FROM `job`")
    columns = {row[0] for row in cursor.fetchall()}
    add_columns = []
    if "source_job_key" not in columns:
        add_columns.append("ADD COLUMN `source_job_key` varchar(32) NULL AFTER `job_id`")
    if "source_url" not in columns:
        add_columns.append("ADD COLUMN `source_url` varchar(255) NULL AFTER `source_job_key`")
    if "dedupe_key" not in columns:
        add_columns.append("ADD COLUMN `dedupe_key` char(40) NULL AFTER `source_url`")
    if add_columns:
        cursor.execute(f"ALTER TABLE `job` {', '.join(add_columns)}")


def ensure_indexes(cursor):
    cursor.execute("SHOW INDEX FROM `job`")
    indexes = {row[2] for row in cursor.fetchall()}
    if "uq_job_dedupe_key" not in indexes:
        cursor.execute("CREATE UNIQUE INDEX `uq_job_dedupe_key` ON `job` (`dedupe_key`)")
    if "uq_job_source_key" not in indexes:
        cursor.execute("CREATE UNIQUE INDEX `uq_job_source_key` ON `job` (`source_job_key`)")


def backfill_dedupe_keys(cursor):
    cursor.execute("SELECT `job_id`, `company`, `job_title`, `address` FROM `job`")
    rows = cursor.fetchall()
    updates = [
        (build_dedupe_key(company, job_title, address), job_id)
        for job_id, company, job_title, address in rows
    ]
    if updates:
        cursor.executemany("UPDATE `job` SET `dedupe_key` = %s WHERE `job_id` = %s", updates)


def merge_duplicate_jobs(cursor):
    cursor.execute(
        """
        SELECT `dedupe_key`, `job_id`, `update_time`
        FROM `job`
        WHERE `dedupe_key` IS NOT NULL
        ORDER BY `dedupe_key`, `update_time` DESC, `job_id` DESC
        """
    )
    groups = defaultdict(list)
    for dedupe_key, job_id, update_time in cursor.fetchall():
        groups[dedupe_key].append((job_id, update_time))

    deleted_count = 0
    for jobs in groups.values():
        if len(jobs) < 2:
            continue

        keeper_id = jobs[0][0]
        duplicate_ids = [job_id for job_id, _ in jobs[1:]]
        for table, target_column in RELATION_TABLES:
            cursor.execute(
                f"SELECT `{target_column}` FROM `{table}` WHERE `job_id` IN ({', '.join(['%s'] * len(duplicate_ids))})",
                tuple(duplicate_ids),
            )
            relation_rows = [(keeper_id, row[0]) for row in cursor.fetchall()]
            if relation_rows:
                cursor.executemany(
                    f"INSERT IGNORE INTO `{table}` (`job_id`, `{target_column}`) VALUES (%s, %s)",
                    relation_rows,
                )

        cursor.execute(
            f"DELETE FROM `job` WHERE `job_id` IN ({', '.join(['%s'] * len(duplicate_ids))})",
            tuple(duplicate_ids),
        )
        deleted_count += len(duplicate_ids)
    return deleted_count


def migrate_database(database):
    conn = connect(database)
    cursor = conn.cursor()
    try:
        ensure_columns(cursor)
        backfill_dedupe_keys(cursor)
        deleted_count = merge_duplicate_jobs(cursor)
        ensure_indexes(cursor)
        conn.commit()
        print(f"{database}: migrated dedupe schema, removed {deleted_count} duplicate rows.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def main():
    for database in (CRAWL_DATABASE, APP_DATABASE):
        migrate_database(database)


if __name__ == "__main__":
    main()
