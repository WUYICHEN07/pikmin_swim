# 流程圖設計：皮克敏水性類型運動換算步數系統

## 1. 使用者流程圖（User Flow）

此流程圖描述了「一般玩家」在前端網頁的操作路徑，以及「穿戴裝置」在背景傳送資料的流程。

```mermaid
flowchart LR
    %% 穿戴裝置的背景流程
    Device([穿戴裝置 / 模擬器]) -.->|1. 發送 JSON 數據| Sync[F-01 接收並同步運動數據]
    Sync -.->|2. F-02 換算為步數| DB[(資料庫)]

    %% 玩家前端操作流程
    Start([使用者開啟網頁]) --> CheckAuth{是否已登入？}
    CheckAuth -->|否| Login[登入 / 註冊頁面]
    Login -->|成功| CheckAuth
    CheckAuth -->|是| Dashboard[首頁 - 個人數據總覽]
    
    Dashboard --> Action{要執行什麼操作？}
    
    Action -->|查看紀錄| History[瀏覽歷史換算紀錄]
    History --> Dashboard
    
    Action -->|切換背景| Theme[設定頁 - 選擇水系主題背景]
    Theme -->|套用新背景| Dashboard
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖詳細說明了您主要負責的核心功能：**F-01 運動數據接入 API 整合** 從接收到儲存的資料流動。

```mermaid
sequenceDiagram
    actor Device as 穿戴裝置 (或模擬器)
    participant API as Flask Route (api.py)
    participant Model as Model (activity.py)
    participant DB as SQLite 資料庫
    
    Device->>API: 1. POST /api/v1/activity (發送 JSON: 運動類型, 時長, 距離...)
    API->>API: 2. 驗證 JSON 格式與必填欄位 (F-01)
    
    alt 資料格式錯誤
        API-->>Device: 400 Bad Request (回傳錯誤訊息)
    else 資料格式正確
        API->>Model: 3. 解析資料並呼叫換算公式
        Model->>Model: 4. 根據水上運動數據換算為「皮克敏步數」 (F-02)
        Model->>DB: 5. INSERT INTO activities (儲存原始數據與換算結果)
        DB-->>Model: 成功儲存
        Model-->>API: 回傳儲存成功結果
        API-->>Device: 6. 200 OK / 201 Created (回傳成功狀態)
    end
```

## 3. 功能清單對照表

根據 PRD 定義的 MVP 範圍，初步規劃的系統功能與對應的 HTTP 方法及預期路徑：

| 功能代號 | 功能說明 | HTTP 方法 | 對應的 URL 路徑 |
| :--- | :--- | :---: | :--- |
| **F-01** | **運動數據接入 API** | `POST` | `/api/v1/activity` |
| F-03 | 系統首頁 (個人數據總覽) | `GET` | `/` 或 `/dashboard` |
| F-04 | 更新個人化水系背景設定 | `POST` | `/settings/theme` |
| F-05 | 使用者登入頁面 | `GET` | `/login` |
| F-05 | 處理使用者登入驗證 | `POST` | `/login` |
| F-05 | 使用者登出 | `GET` / `POST`| `/logout` |

*(註：F-02 換算邏輯為後端內部呼叫的方法，並無直接對外的獨立路由，會在 F-01 接收數據時由 API 連帶呼叫。F-03 的歷史紀錄通常會直接隨首頁的 `GET /` 請求一同由 Jinja2 渲染。)*
