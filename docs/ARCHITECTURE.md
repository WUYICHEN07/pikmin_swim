# 系統架構設計：皮克敏水性類型運動換算步數系統

## 1. 技術架構說明
本專案採用經典的 Web 後端渲染架構，不採用前後端分離，確保開發流程單純、快速且易於維護，適合目前的 MVP 階段。

- **後端框架：Python + Flask**
  - **原因**：Flask 是輕量級框架，上手快、具備高度彈性，非常適合用來快速建立 API 介面與處理路由邏輯（如負責接收運動數據的 F-01 API）。
- **前端模板：Jinja2**
  - **原因**：Flask 內建支援 Jinja2，可在後端直接處理變數替換、條件邏輯與迴圈，將動態資料（如累積步數、換算紀錄）嵌入 HTML 中並渲染給瀏覽器。
- **資料庫：SQLite (搭配 sqlite3 或 SQLAlchemy)**
  - **原因**：無須額外架設資料庫伺服器，資料儲存於本地單一檔案，輕巧且足以應付初期規模的使用者資料與運動紀錄。

**MVC 模式說明**：
- **Model (模型)**：負責定義資料結構（例如 User、ActivityRecord）與資料庫互動，封裝步數換算邏輯等商業規則。
- **View (視圖)**：負責呈現資料給使用者，由 Jinja2 結合 HTML/CSS 構成介面。
- **Controller (控制器)**：由 Flask 的 Routes (路由) 負責，處理使用者的請求（接收 API 資料或頁面訪問）、調用 Model 處理資料，最後將資料傳遞給 View 進行渲染或直接回傳 JSON。

## 2. 專案資料夾結構

```text
pikmin_swim/
├── app/                        ← 主要應用程式目錄
│   ├── __init__.py             ← 初始化 Flask 應用程式
│   ├── models/                 ← 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── user.py             ← 使用者帳號模型
│   │   └── activity.py         ← 運動數據與換算紀錄模型
│   ├── routes/                 ← Flask 路由控制器 (Controller)
│   │   ├── __init__.py
│   │   ├── api.py              ← 處理穿戴裝置發送的運動數據 API (F-01)
│   │   ├── main.py             ← 網站主要頁面路由 (展示步數、個人紀錄)
│   │   └── auth.py             ← 處理註冊、登入邏輯
│   ├── templates/              ← Jinja2 HTML 模板 (View)
│   │   ├── base.html           ← 共用模板 (如導覽列)
│   │   ├── dashboard.html      ← 個人數據總覽與紀錄展示頁 (F-03)
│   │   └── login.html          ← 登入/註冊頁 (F-05)
│   └── static/                 ← CSS / JS 等靜態資源
│       ├── css/
│       │   └── style.css       ← 主要樣式表，包含個人化背景切換設定 (F-04)
│       ├── js/
│       │   └── main.js         ← 處理前端基礎互動
│       └── images/             ← 水性主題背景圖片資源
├── docs/                       ← 專案文件 (PRD, 架構圖等)
│   ├── PRD.md
│   └── ARCHITECTURE.md
├── instance/                   ← 存放本機開發機密或獨立資料庫
│   └── database.db             ← SQLite 資料庫檔案
├── app.py                      ← 系統啟動入口
├── requirements.txt            ← Python 依賴套件清單 (Flask 等)
└── README.md                   ← 專案說明
```

## 3. 元件關係圖

以下展示各元件在系統中如何互相溝通：

```mermaid
graph TD
    %% 角色
    Device[穿戴裝置 / 模擬器]
    Browser[玩家瀏覽器]

    %% 控制器
    subgraph Controller [Flask 路由 (Routes)]
        API_Route[API 路由 api.py]
        Page_Route[頁面路由 main.py]
    end

    %% 模型
    subgraph Model [資料庫模型 (Models)]
        Logic[步數換算邏輯 / 數據驗證]
        DB[(SQLite database.db)]
    end

    %% 視圖
    subgraph View [前端視圖 (Templates)]
        Jinja[Jinja2 模板]
    end

    %% API 數據流 (F-01)
    Device --"1. 發送 JSON 運動數據 (POST)"--> API_Route
    API_Route --"2. 驗證與解析"--> Logic
    Logic --"3. 換算步數並儲存"--> DB
    Logic -.-> API_Route
    API_Route --"4. 回傳成功狀態 (JSON)"--> Device

    %% 頁面訪問流
    Browser --"A. 請求查看數據頁面 (GET)"--> Page_Route
    Page_Route --"B. 查詢歷史紀錄"--> DB
    DB -.-> Page_Route
    Page_Route --"C. 傳送資料"--> Jinja
    Jinja --"D. 渲染完成的 HTML"--> Browser
```

## 4. 關鍵設計決策

1. **獨立 API 路由 (F-01 專屬設計)**
   - **決策**：將負責接收穿戴裝置資料的路由獨立成 `api.py`，與一般網站頁面路由 (`main.py`) 分開。
   - **原因**：因為 API 路由預期接收和回傳的是 JSON 格式，而非 HTML 頁面，獨立出來能提升維護性，且方便實作特定的 JSON 資料格式驗證與日後的擴展。

2. **步數換算邏輯封裝於 Model 之中 (F-02)**
   - **決策**：將水上運動換算為皮克敏步數的數學公式，實作在 `models/activity.py` 中，而非 Controller 裡。
   - **原因**：這屬於系統核心商業邏輯（Business Logic）。封裝在 Model 中能確保日後不管從網頁手動新增，還是透過 API 自動接收，都會經過一致的換算標準。

3. **背景切換透過 CSS class 控制 (F-04)**
   - **決策**：個人化水系背景將透過 Jinja2 在 `<body>` 標籤動態注入對應的 CSS class（如 `class="theme-pool"` 或 `class="theme-ocean"`）來實現。
   - **原因**：這種作法簡單且效能好，無須使用複雜的 JavaScript 框架，僅靠靜態圖片搭配樣式即可達成水性主題切換。
