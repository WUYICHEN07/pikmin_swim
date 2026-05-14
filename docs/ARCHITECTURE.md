# 系統架構設計 (System Architecture)

這份文件根據 PRD 描述的「皮克敏水性類型運動換算步數系統」需求，規劃了整體的技術架構、資料夾結構與元件之間的互動關係。

---

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

1. **採用伺服器端渲染 (SSR) 而非前後端分離**
   - **原因**：為了簡化架構並加快 MVP 的開發速度，不使用 React 或 Vue 等前端框架，而是讓 Flask 與 Jinja2 在後端直接產生完整的 HTML 頁面。這樣可以把重心放在核心邏輯（資料庫與步數轉換）的實作。
2. **獨立的步數轉換引擎模組 (`utils/step_converter.py`)**
   - **原因**：將水上運動（時間、距離、泳姿等）轉換為步數的演算法獨立抽離。未來如果演算法需要升級（例如給予不同泳姿不同的權重），只需要修改這個檔案即可，不會影響到路由和資料庫的結構。
3. **個人化背景設定存於使用者資料表**
   - **原因**：為了實現類似皮克敏介面的自訂背景需求，我們會在 User 的資料表中加入類似 `theme_preference` 的欄位。當使用者登入時，Jinja2 模板就會根據此欄位，動態載入對應的背景 CSS 或圖片，確保個人化體驗。
4. **資料庫讀寫的模組化封裝 (`models/`)**
   - **原因**：為了讓負責歷史紀錄與資料庫管理的成員能專注於開發，將所有的 `SELECT`, `INSERT`, `UPDATE`, `DELETE` (CRUD) 操作封裝在特定的 Python 類別或函數中。路由層不需要寫 SQL 語法，只需呼叫 `record.get_all_by_user()`，提高程式碼的安全性與可讀性。
