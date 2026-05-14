# 流程圖文件 (Flowchart) - 皮克敏水性類型運動換算步數系統

這份文件說明了使用者的操作流程（User Flow）、系統處理資料的序列圖（Sequence Diagram），以及對應的系統功能清單。

## 1. 使用者流程圖（User Flow）

描述使用者進入系統後，可以進行的操作與頁面轉換路徑。

```mermaid
flowchart LR
    A([使用者進入系統]) --> B[個人運動成就看板首頁]
    B --> C{選擇操作}
    
    C -->|輸入游泳數據| D[點擊新增紀錄]
    D --> E[填寫距離與時間]
    E --> F[送出數據進行換算]
    F --> G[畫面即時更新進度條與皮克敏狀態]
    G --> B
    
    C -->|查詢過去紀錄| H[點擊歷史紀錄]
    H --> I[檢視過往轉換明細與累計步數]
    I -->|返回| B
    
    C -->|個人化設定| J[點擊切換背景]
    J --> K[選擇新背景主題]
    K --> L[看板背景即時變更]
    L --> B
```

## 2. 系統序列圖（Sequence Diagram）

描述最核心的「使用者輸入數據並更新看板」的背後運作流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant FlaskAPI as Flask Route (API)
    participant Model as Database Model
    participant DB as SQLite 資料庫

    User->>Browser: 填寫游泳距離與時間並送出
    Browser->>FlaskAPI: POST /api/record (Fetch API 傳送 JSON 數據)
    FlaskAPI->>Model: 呼叫換算邏輯 (如: 距離轉換為步數)
    Model->>DB: INSERT INTO records (儲存單次運動紀錄)
    Model->>DB: UPDATE users (更新玩家總步數)
    DB-->>Model: 確認儲存成功
    Model->>Model: 判斷是否達到下一階皮克敏成長或解鎖成就
    Model-->>FlaskAPI: 回傳最新總步數、成長與成就狀態
    FlaskAPI-->>Browser: 回傳 JSON (包含最新進度與動畫狀態)
    Browser->>Browser: JavaScript 更新進度條寬度與數值
    Browser->>Browser: 觸發皮克敏成長或成就解鎖動畫
    Browser-->>User: 顯示最新成就看板
```

## 3. 功能清單對照表

以下為系統中各主要功能與對應的路由設計：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| **顯示看板首頁** | `/` | `GET` | 透過 Jinja2 渲染個人運動成就看板，包含使用者當前的步數狀態、選擇的背景與皮克敏圖示。 |
| **顯示歷史紀錄頁** | `/history` | `GET` | 透過 Jinja2 渲染歷史運動紀錄清單頁面，讓玩家回顧過去的運動轉換明細。 |
| **送出運動數據** | `/api/record` | `POST` | 接收前端傳來的游泳數據，換算為步數並儲存至資料庫，回傳最新的狀態 JSON 給前端更新畫面。 |
| **切換背景設定** | `/api/background` | `POST` | 接收前端選擇的背景主題，更新資料庫中的使用者設定，並回傳確認訊息。 |
| **取得最新狀態** | `/api/status` | `GET` | 提供前端透過 AJAX 取得目前最新總步數與狀態的介面（用於重新整理或其他非同步需求）。 |
