# 系統架構設計 (Architecture)

這份文件根據 `docs/PRD.md` 規劃了 **Pikmin Swim** 專案的系統架構，為後續的開發提供技術指引。

## 1. 技術架構說明

本專案採用傳統的伺服器端渲染 (Server-Side Rendering) 架構，不進行前後端分離，藉此快速開發並達成 MVP 目標。

### 選用技術與原因
- **後端框架：Flask (Python)** 
  - 輕量且靈活，適合快速開發中小型專案與建構核心步數轉換演算法。
- **模板引擎：Jinja2**
  - 完美整合於 Flask，可以將後端資料無縫嵌入 HTML，減少前端開發的複雜度。
- **資料庫：SQLite (透過 sqlite3 或 SQLAlchemy)**
  - 內建於 Python 且無需額外架設資料庫伺服器，對專案初期的使用者資料與運動紀錄儲存已經非常夠用。

### Flask MVC 模式說明
我們將採用類似 MVC（Model-View-Controller）的架構來組織程式碼：
- **Model (模型)**：負責與 SQLite 資料庫溝通，處理資料的讀寫與業務邏輯（如處理運動紀錄的存取）。
- **View (視圖)**：負責呈現給使用者的畫面，由 Jinja2 搭配 HTML/CSS 以及不同的海洋主題背景組成。
- **Controller (控制器)**：由 Flask 的路由 (Routes) 扮演，負責接收使用者的請求、呼叫步數轉換演算法、從 Model 取得資料，最後傳遞給 View 進行渲染。
# 系統架構設計 (System Architecture)

這份文件根據 PRD 描述的「皮克敏水性類型運動換算步數系統」需求，規劃了整體的技術架構、資料夾結構與元件之間的互動關係。

---
# 系統架構文件 (Architecture) - 皮克敏水性類型運動換算步數系統

## 1. 技術架構說明

### 選用技術與原因
- **後端框架：Python + Flask**
  輕量級且易於上手，非常適合快速打造中小型 Web 專案。它能輕鬆處理使用者的登入請求、表單提交，以及呼叫步數轉換邏輯。
- **模板引擎：Jinja2**
  與 Flask 完美整合的模板引擎。它負責將後端的資料（如使用者的歷史運動紀錄、轉換後的步數）動態渲染進 HTML 中，不需額外引入複雜的前端框架（如 React/Vue）就能做出豐富的介面。
- **資料庫：SQLite**
  內建於 Python 中，以單一檔案的形式存在。不需要繁瑣的資料庫伺服器架設步驟，極大降低了團隊開發與本地端測試的門檻。

### Flask MVC 模式說明
雖然 Flask 本身是微框架，但我們將採用類似 MVC (Model-View-Controller) 的架構來明確分工：
- **Model (資料模型)**：負責定義 SQLite 的資料表結構（使用者、運動紀錄、步數轉換紀錄），並實作負責存取資料庫的 CRUD 操作函數。
- **View (視圖)**：由 Jinja2 模板組成，包含系統的操作介面、表單，以及能客製化的皮克敏風格背景。
- **Controller (控制器/路由)**：由 Flask 的 Routes (`@app.route`) 擔任，負責接收從瀏覽器傳來的 HTTP 請求，調用步數換算邏輯與 Model，然後把處理結果交給 View 去渲染。

---

## 2. 專案資料夾結構

專案將採取清晰的模組化結構，將模型、路由、模板與靜態資源分離。

```text
pikmin_swim/
├── app/                      ← 應用程式的主要目錄
│   ├── __init__.py           ← 初始化 Flask App 與設定
│   ├── models/               ← 資料庫模型 (Model)
│   │   └── user_record.py    ← 定義使用者與運動紀錄的資料表結構與操作
│   ├── routes/               ← Flask 路由 (Controller)
│   │   ├── main.py           ← 首頁與儀表板路由
│   │   ├── convert.py        ← 步數轉換核心邏輯路由
│   │   └── auth.py           ← 使用者登入/註冊路由
│   ├── templates/            ← Jinja2 HTML 模板 (View)
│   │   ├── base.html         ← 共用模板（導覽列、頁尾）
│   │   ├── index.html        ← 首頁/儀表板
│   │   ├── login.html        ← 登入/註冊頁面
│   │   └── convert.html      ← 輸入運動數據並顯示轉換結果的頁面
│   └── static/               ← 靜態資源 (CSS / JS / 圖片)
│       ├── css/
│       │   └── style.css     ← 主要樣式檔
│       ├── js/
│       │   └── main.js       ← 簡易的前端互動邏輯
│       └── images/           ← 海洋/水上主題背景圖片存放區
├── instance/                 ← 放置不進版本控制的實體資料
│   └── database.db           ← SQLite 資料庫檔案
├── docs/                     ← 開發文件目錄 (PRD, Architecture 等)
├── app.py                    ← 應用程式入口點，負責啟動伺服器
├── requirements.txt          ← Python 依賴套件清單
└── README.md                 ← 專案說明文件
為了保持程式碼的整潔與好維護，我們將專案拆分成以下結構：

```text
pikmin_swim/
├── app/                      # 應用程式主要資料夾
│   ├── models/               # (Model) 資料庫模型與 CRUD 操作
│   │   ├── __init__.py
│   │   ├── user.py           # 使用者資料表管理
│   │   ├── record.py         # 運動紀錄與轉換紀錄管理
│   │   └── db_helper.py      # 資料庫連線與輔助函數
│   ├── routes/               # (Controller) Flask 路由與邏輯
│   │   ├── __init__.py
│   │   ├── auth.py           # 登入與註冊路由
│   │   ├── dashboard.py      # 歷史紀錄與主控台路由
│   │   └── convert.py        # 接收運動數據並呼叫換算引擎的路由
│   ├── templates/            # (View) Jinja2 HTML 模板
│   │   ├── base.html         # 包含共用導覽列與背景佈景設定的基礎模板
│   │   ├── index.html        # 首頁 / 登入頁
│   │   ├── dashboard.html    # 歷史紀錄列表頁
│   │   └── add_record.html   # 新增運動紀錄表單頁
│   ├── static/               # CSS / JS 靜態資源
│   │   ├── css/
│   │   │   └── style.css     # 客製化皮克敏風格樣式
│   │   ├── js/
│   │   │   └── main.js       # 處理簡單介面互動
│   │   └── images/           # 各種可替換的背景圖檔
│   └── utils/                # 輔助工具
│       └── step_converter.py # 步數轉換引擎核心演算法
├── instance/                 # 存放不會進版本控制的敏感或本地資料
│   └── database.db           # SQLite 本地端資料庫檔案
├── docs/                     # 專案文件 (PRD, 架構文件等)
├── .gitignore
├── requirements.txt          # Python 套件相依性清單
└── app.py                    # Flask 應用程式入口點
```

---

## 3. 元件關係圖

以下展示了系統各元件在處理使用者請求時的互動關係：

```mermaid
sequenceDiagram
    participant Browser as 瀏覽器 (使用者)
    participant Route as Flask Route (Controller)
    participant Algorithm as 轉換演算法
    participant Model as Model (資料存取)
    participant DB as SQLite (資料庫)
    participant Template as Jinja2 (View)

    Browser->>Route: 1. POST 輸入游泳時長 (HTTP Request)
    Route->>Algorithm: 2. 呼叫轉換邏輯
    Algorithm-->>Route: 3. 回傳計算後步數
    Route->>Model: 4. 寫入轉換紀錄
    Model->>DB: 5. INSERT 紀錄
    DB-->>Model: 6. 確認寫入成功
    Model-->>Route: 7. 回傳結果
    Route->>Template: 8. 傳遞資料並渲染畫面
    Template-->>Browser: 9. 回傳 HTML 頁面 (HTTP Response)
以下展示使用者在瀏覽器上的操作，是如何經過 Flask 路由，最終與資料庫和模板互動的流程：

```mermaid
flowchart TD
    Browser[瀏覽器 (使用者介面)]
    
    subgraph Controller
        Route[Flask Route (app.py / routes)]
        Converter[步數轉換引擎 (step_converter.py)]
    end

    subgraph Model
        SQLite[(SQLite 資料庫)]
        DBModel[資料模型與 CRUD (models/)]
    end

    subgraph View
        Jinja[Jinja2 HTML 模板 (templates/)]
    end

    %% 請求流程
    Browser -- "1. 提交運動紀錄表單 (POST)" --> Route
    Route -- "2. 呼叫轉換演算法" --> Converter
    Converter -- "3. 回傳計算後步數" --> Route
    Route -- "4. 呼叫新增功能" --> DBModel
    DBModel -- "5. 寫入資料" --> SQLite
    
    %% 渲染流程
    SQLite -. "6. 讀取歷史紀錄" .-> DBModel
    DBModel -. "7. 回傳紀錄列表" .-> Route
    Route -- "8. 傳遞資料與背景設定" --> Jinja
    Jinja -- "9. 渲染出 HTML 網頁" --> Browser
```

---

## 4. 關鍵設計決策

1. **整合路由與演算法的設計**
   - **決策**：將步數核心轉換演算法獨立封裝為一個模組，由 `convert.py` 路由呼叫，而不是直接寫死在路由中。
   - **原因**：為了確保未來若轉換邏輯變更（例如支援不同泳姿有不同權重），可以單獨測試與修改演算法模組，而不影響 Web 路由。
2. **採用 Jinja2 處理背景切換邏輯**
   - **決策**：海洋主題背景的狀態透過後端傳遞變數給 Jinja2 模板，由模板根據變數動態套用對應的 CSS 類別。
   - **原因**：可以避免編寫複雜的 JavaScript 狀態管理，讓頁面渲染更直接，並且狀態可以隨使用者的偏好設定記錄在資料庫中。
3. **SQLite 資料庫存放於 `instance/` 資料夾**
   - **決策**：將 `database.db` 放在獨立的 `instance/` 目錄並將其加入 `.gitignore`（或只保存空架構）。
   - **原因**：避免將真實的使用者資料（包含密碼雜湊）上傳至公開或共用的 Git 儲存庫，增強系統安全性與隱私性。
1. **採用伺服器端渲染 (SSR) 而非前後端分離**
   - **原因**：為了簡化架構並加快 MVP 的開發速度，不使用 React 或 Vue 等前端框架，而是讓 Flask 與 Jinja2 在後端直接產生完整的 HTML 頁面。這樣可以把重心放在核心邏輯（資料庫與步數轉換）的實作。
2. **獨立的步數轉換引擎模組 (`utils/step_converter.py`)**
   - **原因**：將水上運動（時間、距離、泳姿等）轉換為步數的演算法獨立抽離。未來如果演算法需要升級（例如給予不同泳姿不同的權重），只需要修改這個檔案即可，不會影響到路由和資料庫的結構。
3. **個人化背景設定存於使用者資料表**
   - **原因**：為了實現類似皮克敏介面的自訂背景需求，我們會在 User 的資料表中加入類似 `theme_preference` 的欄位。當使用者登入時，Jinja2 模板就會根據此欄位，動態載入對應的背景 CSS 或圖片，確保個人化體驗。
4. **資料庫讀寫的模組化封裝 (`models/`)**
   - **原因**：為了讓負責歷史紀錄與資料庫管理的成員能專注於開發，將所有的 `SELECT`, `INSERT`, `UPDATE`, `DELETE` (CRUD) 操作封裝在特定的 Python 類別或函數中。路由層不需要寫 SQL 語法，只需呼叫 `record.get_all_by_user()`，提高程式碼的安全性與可讀性。
  - **原因**：Flask 輕量且彈性高，非常適合用來快速開發中小型應用程式與 API。對於這個主要處理「數據換算」和「看板展示」的專案來說，不會有過多的效能負擔。
- **前端模板與渲染：Jinja2 + Vanilla JS (Fetch API)**
  - **原因**：由 Flask 搭配 Jinja2 處理初始的 HTML 頁面渲染（如基礎結構、樣式匯入），而看板中的「即時數據更新」與「進度條動畫」則透過前端的 Fetch API 向 Flask 請求 JSON 資料來動態更新。這樣可以達到畫面不閃爍、平順更新的體驗，符合「不需要前後端分離」的技術限制。
- **資料庫：SQLite**
  - **原因**：免安裝、輕量化，資料直接存放在本地檔案，對於 MVP 階段的個人運動紀錄查詢與儲存已十分足夠。

### Flask MVC 模式說明
本專案的設計概念對應了 MVC (Model-View-Controller) 架構：
- **Model（資料庫模型）**：負責與 SQLite 互動，定義與存取運動紀錄、使用者累積步數、解鎖的成就與背景設定。
- **View（視圖）**：使用 Jinja2 模板渲染 HTML 頁面，結合 CSS 提供與皮克敏風格相似的介面，以及透過 JavaScript 更新畫面。
- **Controller（控制器/路由）**：Flask 的 Routes 扮演控制器的角色，接收來自前端的 HTTP 請求（例如使用者提交游泳數據），呼叫 Model 進行邏輯運算與存檔，最後將結果回傳（渲染 View 或是回傳 JSON 給 Fetch API）。

## 2. 專案資料夾結構

建議的資料夾結構如下，以模組化方式分離職責：

```text
pikmin_swim/
├── app/
│   ├── __init__.py      # Flask 應用程式工廠，初始化 app 
│   ├── models/          # Model 模組
│   │   ├── __init__.py
│   │   └── database.py  # SQLite 資料表定義與操作邏輯 (如 User, Record)
│   ├── routes/          # Controller 模組
│   │   ├── __init__.py
│   │   ├── page.py      # 負責渲染 Jinja2 頁面的路由 (如首頁、歷史紀錄頁)
│   │   └── api.py       # 負責處理 Fetch API 請求的路由 (如上傳數據)
│   ├── templates/       # View 模組 (Jinja2 HTML 檔案)
│   │   ├── base.html    # 頁面共用佈局 (Layout)
│   │   ├── index.html   # 個人運動成就看板主頁
│   │   └── history.html # 歷史紀錄查詢頁
│   └── static/          # 前端靜態資源
│       ├── css/
│       │   └── style.css  # 皮克敏風格的樣式表
│       ├── js/
│       │   └── dashboard.js # 處理 Fetch API 呼叫、進度條動畫與背景切換
│       └── images/      # 存放背景圖、皮克敏成長圖示、成就徽章等
├── instance/
│   └── pikmin.db        # SQLite 資料庫檔案 (運行時自動產生)
├── docs/
│   ├── PRD.md           # 產品需求文件
│   └── ARCHITECTURE.md  # 系統架構文件 (本文)
├── requirements.txt     # Python 套件相依清單 (Flask 等)
└── app.py               # 專案入口點，啟動 Flask 伺服器
```

## 3. 元件關係圖

以下展示使用者在瀏覽器上操作時，系統各元件如何互動：

```mermaid
sequenceDiagram
    participant Browser as 瀏覽器 (Frontend)
    participant FlaskPage as Flask Route (Page)
    participant FlaskAPI as Flask Route (API)
    participant Model as Database Model
    participant SQLite as SQLite DB

    %% 首次載入頁面
    Browser->>FlaskPage: GET / (請求看板首頁)
    FlaskPage->>Model: 讀取使用者設定 (如背景)
    Model->>SQLite: 查詢 DB
    SQLite-->>Model: 回傳資料
    Model-->>FlaskPage: 使用者資料
    FlaskPage-->>Browser: 回傳 index.html (Jinja2 渲染)

    %% 送出運動數據並即時更新
    Browser->>FlaskAPI: POST /api/record (Fetch API: 傳送游泳數據)
    FlaskAPI->>Model: 換算步數並儲存紀錄
    Model->>SQLite: INSERT 運動紀錄 & UPDATE 總步數
    SQLite-->>Model: 確認儲存
    Model-->>FlaskAPI: 傳回最新總步數與成長狀態
    FlaskAPI-->>Browser: 回傳 JSON (新進度與解鎖成就)
    Note over Browser: JavaScript 更新進度條<br/>顯示皮克敏成長動畫
```

## 4. 關鍵設計決策

1. **混合式渲染 (Hybrid Rendering) 提升使用者體驗**
   - **決策**：不採用完全的 SPA (單頁應用程式)，而是以 Jinja2 渲染主要框架，但在核心的「看板數據與進度條」使用 JavaScript Fetch API 來實作。
   - **原因**：這樣可以在保持 Flask 架構簡單的同時，讓進度條更新時畫面不會重整，增強類似遊戲中的即時互動感與沉浸感。
2. **數據換算邏輯封裝於後端**
   - **決策**：將「游泳距離/時間」轉換為「步數」的邏輯實作於 Flask 的 Controller/Model 中，而不是寫在前端 JavaScript。
   - **原因**：確保換算邏輯的安全性與一致性，未來若換算公式需要調整，只需修改後端程式碼即可，前端單純負責展示結果，也方便進行單元測試。
3. **圖片資源與背景的動態載入**
   - **決策**：皮克敏成長狀態圖示及不同背景圖存放在 `static/images/`，但在資料庫中僅儲存使用者選擇的背景檔名或 ID。前端透過 API 取得狀態後，用 JS 動態更改 CSS 的 background-image。
   - **原因**：能有效降低資料庫儲存負擔，並且可以輕易擴充新的背景主題與皮克敏圖示，不需更動資料表結構。
