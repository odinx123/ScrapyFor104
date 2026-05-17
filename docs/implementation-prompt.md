# 後續實作提示

目前第一階段已完成環境設定、MySQL Docker schema、Scrapy 批次 pipeline、GUI 批次查詢。

下一階段建議處理：

1. 將 `GUI.Gui.__init__` 拆成 layout 建立與資料載入兩段。
2. 用 background thread 載入 MySQL 與 TF-IDF，Tkinter UI 更新只透過 `root.after()` 回主執行緒。
3. 將 Redis 設計成可選模式：
   - `SCRAPY104_ITEM_BUFFER=mysql`: 現有批次 MySQL pipeline。
   - `SCRAPY104_ITEM_BUFFER=redis`: Scrapy 只推 JSON item 到 Redis stream/list。
   - `scripts/consume_redis_items.py`: 批次讀 Redis 並使用同一份 MySQL writer 落庫。
4. 把 SQL schema 移到單一 canonical migration，避免 `job104`、`jobdatabase`、dump file schema 分歧。
5. 補測試：
   - salary parser unit tests。
   - pipeline batch writer 對 mock cursor 的 SQL 行為測試。
   - `JobDatabase.get_jobInfos_by_ids()` 對測試資料庫的整合測試。
