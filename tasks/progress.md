# Progress

| Task | Status | Notes |
| --- | --- | --- |
| Repo/environment audit | verified | Confirmed no PATH Python, pyenv, or conda; Codex bundled Python used only for static checks. |
| pyenv setup files | verified | Installed pyenv-win, Python 3.11.9, and project `.venv`; added `.python-version` and setup script. |
| Docker MySQL/Redis | verified | Docker Compose starts MySQL and Redis; verified `job104` and `jobdatabase` exist. |
| Scrapy batch pipeline | verified | Pipeline now buffers items and writes batches with parameterized SQL; Scrapy imports and `scrapy check` pass. |
| 104 search API parser | verified | Replaced stale HTML selector parsing with `/jobs/search/api/jobs`; live crawl scraped items again. |
| GUI query batching | verified | Added `get_jobInfos_by_ids()` and switched GUI hot paths to bulk reads; GUI module import passes. |
| GUI startup data loading | verified | UI now loads existing jobs by real database IDs instead of assuming IDs 1-9; empty lists show a clear no-data message. |
| UI database sync | verified | Added `scripts/sync_app_database.py` and synced `job104` into `jobdatabase`; UI database now has 437 jobs. |
| Job dedupe | verified | Added source job tracking plus normalized company/title/address `dedupe_key`; pipeline now upserts duplicate/reposted jobs and refreshes relation tables. |
| Verification | verified | Current UI/data-path syntax checks, GUI import, Docker service status, MySQL counts, and recommendation data preparation verified. |

## Known Follow-Ups

- Install or expose `pyenv` in PATH on this Windows account.
- Convert Tkinter data loading to a background worker.
- Add optional Redis item queue after the MySQL batch writer is stable.
