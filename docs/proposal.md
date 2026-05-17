# ScrapyFor104 改造提案

## 目標

第一階段先解掉三個最明確的阻塞點：

1. 用 pyenv 固定 Python 版本，讓專案從舊的 Anaconda 使用方式轉成可重現環境。
2. 降低爬蟲寫入 MySQL 的等待時間，避免每筆 item 都同步執行多次 SQL 與 commit。
3. 降低 Tkinter 啟動時的 MySQL 查詢成本，先移除查詢層的 N+1 pattern。

## 現況問題

- Scrapy pipeline 每一筆職缺都會同步寫 job、維度表、關聯表，並且每筆 commit 一次。
- SQL 使用 f-string 拼接，遇到特殊字元時容易失敗，也有 SQL injection 風險。
- GUI 啟動時會同步讀 MySQL，推薦功能還會把全量職缺逐筆補關聯資料。
- DB 帳密與 database 名稱硬編碼在多個檔案。
- 專案沒有固定 Python 版本、Docker MySQL/Redis 設定與環境範例。

## 第一階段範圍

- 新增 `.python-version`、`scripts/setup_pyenv.ps1`、`.env.example`。
- 新增 `docker-compose.yml`，提供 MySQL 8 與 Redis 7。
- 新增 Docker MySQL 初始化 schema，建立 `job104` 與 `jobdatabase`。
- Scrapy pipeline 改成記憶體 batch buffer，再批次寫入 MySQL。
- Scrapy 設定改由環境變數控制 DB、並調整下載延遲與 domain concurrency。
- `queryData.JobDatabase` 新增批次讀取職缺與關聯資料的方法。
- GUI 改用批次讀取，並移除部分全域 `db` 依賴。

## 暫不納入

- 完整 GUI 背景執行緒載入與 loading state。
- Redis item queue consumer。
- Alembic/SQL migration 系統。
- 大規模分層重構與套件化。

Redis 目前先保留在 Docker 架構中。單機爬蟲的主要瓶頸是同步 MySQL pipeline；先用記憶體批次寫入可以少引入一個長駐 consumer，風險較低。
