# ScrapyFor104 第一階段設計

## 環境

- Python 版本固定為 `3.11.9`，由 `.python-version` 管理。
- `scripts/setup_pyenv.ps1` 負責 `pyenv install`、`pyenv local`、建立 `.venv` 與安裝 `requirements.txt`。
- DB 連線改走 `SCRAPY104_*` 環境變數，預設值對應本機 Docker。

## Docker

`docker-compose.yml` 提供：

- `mysql`: MySQL 8.0，預設 root 密碼 `9879`，初始化 `job104` 與 `jobdatabase`。
- `redis`: Redis 7，先作為下一階段 queue/buffer 的基礎服務。

MySQL 使用 `--lower-case-table-names=1`，降低 Windows 舊資料與 Linux Docker 在資料表大小寫上的落差。

## 爬蟲寫入

原本 pipeline 是每筆 item 立即做多次 SQL 與一次 commit。新的 pipeline：

1. `process_item()` 只做資料 normalize，放入 `self.buffer`。
2. buffer 達到 `SCRAPY104_PIPELINE_BATCH_SIZE` 後 flush。
3. flush 時批次 `INSERT IGNORE` job、維度表與關聯表。
4. 每批只 commit 一次。
5. 所有資料庫值改用 parameterized query。

這個設計仍然是單進程、記憶體 buffer。若之後爬取量變大或 GUI/分析需要和爬蟲完全解耦，再把 pipeline 改成 Redis list/stream，另寫 consumer 批次落 MySQL。

## GUI 查詢

`JobDatabase.get_jobInfo_by_id()` 原本每個 job 會做 1 次主表查詢與 5 次關聯查詢。新的 `get_jobInfos_by_ids()`：

1. 一次取回多個 job 主表資料。
2. 每種關聯各查一次。
3. 依 job_id 組回原本 GUI 使用的 dict 格式。

這會明顯降低啟動與推薦功能讀取資料時的查詢數量。下一階段再把 Tkinter 啟動流程改成先畫空視窗，再用背景 thread 載入資料。
