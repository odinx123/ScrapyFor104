from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app_config import APP_DATABASE, CRAWL_DATABASE, db_config
from queryData.jobQuery import JobDatabase
from scripts.migrate_job_dedupe import migrate_database


def main():
    migrate_database(CRAWL_DATABASE)
    migrate_database(APP_DATABASE)

    source_db = JobDatabase(**db_config(CRAWL_DATABASE))
    target_db = JobDatabase(**db_config(APP_DATABASE))

    source_count = source_db.get_job_count()
    if source_count == 0:
        raise SystemExit(f"No rows found in source database: {CRAWL_DATABASE}")

    before_count = target_db.get_job_count()
    target_db.move_data_from(CRAWL_DATABASE)
    after_count = target_db.get_job_count()

    print(
        f"Synced {CRAWL_DATABASE} -> {APP_DATABASE}: "
        f"{before_count} rows before, {after_count} rows after."
    )


if __name__ == "__main__":
    main()
