# 路由設計文件 (API Design)：皮克敏水性類型運動換算步數系統

這份文件規劃了 Flask 應用程式中所有的 URL 路由、對應的 Jinja2 模板，以及外部 API 串接端點。
# 路由設計：皮克敏水性類型運動換算步數系統
# 路由設計 (Routes Design)

這份文件根據 PRD、架構文件與流程圖，定義了 Pikmin Swim 系統所有的 URL 路由、處理邏輯及對應的 Jinja2 模板。
# 路由設計 (API Design)

本文件根據 PRD、系統架構與資料庫設計，詳細規劃了系統的所有 URL 路由、對應的處理邏輯與渲染的 HTML 模板。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 登入 | GET | `/` | `index.html` | 顯示系統介紹與登入/註冊表單 |
| 處理登入 | POST | `/login` | — | 驗證使用者並將狀態寫入 session，成功後導向 `/dashboard` |
| 運動儀表板 | GET | `/dashboard` | `dashboard.html` | 顯示總步數、AI 生成的水下皮克敏與背景 |
| 運動數據輸入頁 | GET | `/record` | `record.html` | 顯示水上運動數據的手動輸入表單 |
| 建立運動紀錄 | POST | `/record` | — | 接收數據，呼叫換算引擎，寫入 DB 並導向 `/dashboard` |
| 歷史紀錄 | GET | `/history` | `history.html` | 顯示使用者的所有運動紀錄清單 |
| 更新背景主題 | POST | `/settings/background`| — | 更新 `users.current_background` 並導向 `/dashboard` |
| (預留) 手錶資料同步 | POST | `/api/sync` | — | 接收外部 JSON 數據，儲存並回傳狀態 |

## 2. 每個路由的詳細說明

### `GET /`
- **處理邏輯**：檢查 session 是否已登入，若已登入則重新導向到 `/dashboard`，否則渲染首頁。
- **輸出**：渲染 `index.html`。

### `POST /login`
- **輸入**：表單欄位 `username`。
- **處理邏輯**：呼叫 `User.get_by_id()`（或用名稱查詢），若不存在則自動 `User.create()`，最後將 user_id 存入 Flask session。
- **輸出**：`redirect('/dashboard')`。

### `GET /dashboard`
- **處理邏輯**：需登入。取得當前使用者的 `total_steps` 與 `current_background`。
- **輸出**：渲染 `dashboard.html`，將步數與背景變數傳遞給 Jinja2 模板（由前端進行 UI 美化與 AI 素材展示）。

### `POST /record`
- **輸入**：表單欄位 `sport_type`, `distance`, `duration`。
- **處理邏輯**：
  1. 依據 `sport_type` 計算換算後的步數。
  2. 呼叫 `Activity.create()` 儲存紀錄。
  3. 呼叫 `User.update_steps()` 累加總步數。
- **輸出**：`redirect('/dashboard')`。

### `POST /settings/background`
- **輸入**：表單欄位 `background_theme`（例如：'ocean_default', 'coral_reef' 等）。
- **處理邏輯**：呼叫 `User.update_background()` 寫入 DB。
- **輸出**：`redirect('/dashboard')`。

### `POST /api/sync`
- **輸入**：JSON 格式的運動數據。
- **處理邏輯**：驗證身分後，進行與 `POST /record` 相同的換算與儲存。
- **輸出**：回傳 JSON 回應（例如 `{"status": "success", "steps_added": 1200}`）。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 中，並繼承共用的基礎版型：

- `base.html`：包含 HTML 骨架、共用 CSS (如海洋風樣式)、共用導覽列。
- `index.html`：繼承 `base.html`，首頁介紹與登入介面。
- `dashboard.html`：繼承 `base.html`，展示步數成就與 AI 水下場景的核心頁面。
- `record.html`：繼承 `base.html`，輸入水上運動數據的表單頁面。
- `history.html`：繼承 `base.html`，以表格或清單列出歷史活動。
| :--- | :---: | :--- | :--- | :--- |
| **運動數據接入 API** | **POST** | `/api/v1/activity` | — | **[F-01]** 接收穿戴裝置 JSON 數據，驗證後呼叫換算並存入 DB |
| 系統首頁 / 總覽 | GET | `/` | `dashboard.html` | **[F-03]** 顯示個人累積步數與運動歷史紀錄清單 |
| 切換背景主題 | POST | `/settings/theme` | — | **[F-04]** 接收表單更新背景主題，完成後重導向回首頁 |
| 註冊頁面 | GET | `/register` | `register.html` | **[F-05]** 顯示註冊表單 |
| 處理註冊 | POST | `/register` | — | 接收註冊資料，建立帳號後重導向至登入頁 |
| 登入頁面 | GET | `/login` | `login.html` | **[F-05]** 顯示登入表單 |
| 處理登入 | POST | `/login` | — | 驗證帳號密碼，成功後重導向至首頁 |
| 處理登出 | GET | `/logout` | — | 清除登入狀態，重導向至登入頁 |

## 2. 每個路由的詳細說明

### 2.1 API 路由 (`app/routes/api.py`)

- **POST `/api/v1/activity` (您負責的核心功能 F-01)**
  - **輸入**：JSON 格式的運動數據，需包含 `user_id`, `activity_type`, `duration_minutes`，可選 `distance_meters`, `heart_rate_avg`。
  - **處理邏輯**：
    1. 驗證資料是否為有效的 JSON。
    2. 檢查必填欄位是否存在且型態正確。
    3. 呼叫 `Activity.create()` 將數據寫入資料庫並執行步數換算 (F-02)。
  - **輸出**：回傳 JSON `{"status": "success", "converted_steps": 1200}`，HTTP 狀態碼 `201 Created`。
  - **錯誤處理**：資料缺少或格式錯誤時，回傳 `400 Bad Request` 與錯誤訊息 JSON。

### 2.2 主要頁面路由 (`app/routes/main.py`)

- **GET `/`**
  - **輸入**：無（依賴 session 中的登入狀態）。
  - **處理邏輯**：從 session 取得目前登入的 user_id，呼叫 `User.get_by_id()` 取得使用者資料（含主題設定），並呼叫 `Activity.get_total_steps_by_user()` 取得總步數，以及 `Activity.get_by_user()` 取得歷史紀錄列表。
  - **輸出**：渲染 `dashboard.html`。
  - **錯誤處理**：未登入則重導向至 `/login`。

- **POST `/settings/theme`**
  - **輸入**：表單欄位 `theme` (如 'ocean', 'pool')。
  - **處理邏輯**：呼叫 `User.update_theme()` 更新資料庫設定，更新 session 中的偏好。
  - **輸出**：重導向至 `/`。

### 2.3 帳號驗證路由 (`app/routes/auth.py`)

- **GET / POST `/login` & `/register` & `/logout`**
  - 處理標準的 Flask session 登入、註冊邏輯。
  - 密碼需透過 `werkzeug.security` 進行 hash 處理。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄下：

1. **`base.html`**：共用基礎模板。包含 HTML 的 `<head>`、引入 CSS/JS，以及共用的導覽列 (Navbar)。
2. **`dashboard.html`**：繼承自 `base.html`。首頁內容，顯示總累積步數的大字、背景主題動態切換，以及下方的歷史運動紀錄表格。
3. **`login.html`**：繼承自 `base.html`。包含 Email 與密碼輸入框。
4. **`register.html`**：繼承自 `base.html`。包含使用者名稱、Email 與密碼輸入框。
| --- | --- | --- | --- | --- |
| 首頁 / 儀表板 | GET | `/` | `templates/index.html` | 顯示當前累積步數與個人海洋背景 |
| 註冊頁面 | GET | `/register` | `templates/register.html` | 顯示註冊表單 |
| 註冊邏輯 | POST | `/register` | — | 接收註冊表單，寫入 DB 並重導向 |
| 登入頁面 | GET | `/login` | `templates/login.html` | 顯示登入表單 |
| 登入邏輯 | POST | `/login` | — | 驗證帳號密碼並建立 Session |
| 登出邏輯 | GET | `/logout` | — | 清除 Session 並重導向至登入頁 |
| 轉換紀錄頁面 | GET | `/convert` | `templates/convert.html` | 顯示輸入游泳數據的表單 |
| 執行轉換邏輯 | POST | `/convert` | — | 處理演算法轉換、存入 DB 並重導向 |
| 歷史紀錄頁面 | GET | `/history` | `templates/history.html` | 檢視過去的所有轉換紀錄 |
| 更改背景邏輯 | POST | `/background` | — | 接收背景選項，更新 DB 並重導向 |

## 2. 每個路由的詳細說明

### 首頁 / 儀表板 (`GET /`)
- **輸入**：無。
- **處理邏輯**：檢查使用者是否登入（Session），呼叫 `SwimRecord.get_total_steps_by_user()` 取出總步數，並讀取 `users` 表中的 `preferred_background`。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：未登入則重導向至 `/login`。

### 註冊 (`POST /register`)
- **輸入**：表單欄位 `username`, `password`。
- **處理邏輯**：驗證欄位不可為空，將密碼雜湊處理後，呼叫 `User.create()`。
- **輸出**：成功則重導向 `/login`，失敗（帳號重複）則重新渲染 `register.html` 並顯示錯誤訊息。

### 轉換邏輯 (`POST /convert`)
- **輸入**：表單欄位 `swim_duration` 或 `stroke_count`。
- **處理邏輯**：透過步數核心轉換演算法算出 `converted_steps`，呼叫 `SwimRecord.create()` 存入資料庫。
- **輸出**：成功後使用 Flash 傳遞成功訊息，重導向至 `/`。
- **錯誤處理**：若輸入資料格式錯誤，顯示錯誤訊息並重新渲染 `convert.html`。

### 更改背景 (`POST /background`)
- **輸入**：表單欄位 `bg_choice`（如 `ocean_blue`, `coral_reef`）。
- **處理邏輯**：呼叫 `User.update_background()` 更新資料庫設定。
- **輸出**：重導向回上一頁（通常是首頁）。

## 3. Jinja2 模板清單

以下為後續需開發的 HTML 模板檔案，皆存放在 `app/templates/` 中：

1. **`base.html`**：共用佈局（包含 HTML head、導覽列、頁尾），其他模板皆繼承此檔。
2. **`index.html`**：首頁，繼承自 `base.html`，顯示累積步數與動態載入背景。
3. **`login.html`**：登入表單，繼承自 `base.html`。
4. **`register.html`**：註冊表單，繼承自 `base.html`。
5. **`convert.html`**：輸入游泳數據轉換步數的表單，繼承自 `base.html`。
6. **`history.html`**：以表格方式顯示歷史紀錄，繼承自 `base.html`。

## 4. 路由骨架程式碼
請參考 `app/routes/` 資料夾內的 `main.py`, `auth.py`, `convert.py`，目前僅包含函式定義與註解。
| :--- | :--- | :--- | :--- | :--- |
| 首頁重導向 | GET | `/` | — | 判斷登入狀態，重導向至 `/dashboard` 或 `/login` |
| 登入頁面 | GET | `/login` | `templates/auth/login.html` | 顯示登入表單 |
| 執行登入 | POST | `/login` | — | 驗證帳號密碼，成功則重導向至 `/dashboard` |
| 註冊頁面 | GET | `/register` | `templates/auth/register.html` | 顯示註冊帳號表單 |
| 執行註冊 | POST | `/register` | — | 寫入資料庫建立使用者，重導向至 `/login` |
| 登出 | GET | `/logout` | — | 清除 Session，重導向至 `/login` |
| 個人主控台 | GET | `/dashboard` | `templates/dashboard/index.html` | 顯示所有歷史紀錄、換算步數與客製化背景 |
| 變更背景主題 | POST | `/settings/theme`| — | 更新使用者的背景偏好，重導向至 `/dashboard` |
| 新增紀錄頁面 | GET | `/records/new` | `templates/records/new.html`| 顯示新增水上運動數據的表單 |
| 建立運動紀錄 | POST | `/records` | — | 接收表單、呼叫轉換引擎並寫入 DB，重導至 `/dashboard` |
| 刪除運動紀錄 | POST | `/records/<id>/delete`| — | 刪除指定紀錄與其轉換紀錄，重導至 `/dashboard` |

---

## 2. 每個路由的詳細說明

### 2.1 驗證與使用者授權 (`/login`, `/register`, `/logout`)
- **GET /login & /register**
  - **輸入**：無。
  - **處理邏輯**：顯示對應的 HTML 視圖。如果已登入則直接重導向 `/dashboard`。
- **POST /register**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：呼叫 `User.create()`，若帳號已存在則閃現錯誤訊息並重新渲染註冊頁面。
- **POST /login**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：查詢 `User.get_by_username()` 並比對密碼，成功則設定 `session['user_id']`。

### 2.2 主控台與設定 (`/dashboard`, `/settings/theme`)
- **GET /dashboard**
  - **輸入**：Session 中的 `user_id`。
  - **處理邏輯**：呼叫 `SportsRecord.get_by_user_id(user_id)` 取得歷史資料，並統計總步數。
  - **輸出**：渲染 `dashboard/index.html`。
- **POST /settings/theme**
  - **輸入**：表單欄位 `theme_name`。
  - **處理邏輯**：呼叫 `User.update_theme()`，更新後重導回 `/dashboard`。

### 2.3 運動紀錄管理 (`/records`)
- **GET /records/new**
  - **輸入**：無。
  - **處理邏輯**：需登入。顯示輸入 `sport_type`, `distance_m`, `duration_min` 的表單。
- **POST /records**
  - **輸入**：表單提交運動數據。
  - **處理邏輯**：
    1. 呼叫 `SportsRecord.create()` 存入基本數據。
    2. 呼叫轉換引擎 `step_converter.py` 將數據轉為步數。
    3. 呼叫 `StepConversion.create()` 存入步數。
- **POST /records/<id>/delete**
  - **輸入**：URL 參數 `id`。
  - **處理邏輯**：驗證該紀錄是否屬於當前登入者，確認後呼叫 `SportsRecord.delete()`。

---

## 3. Jinja2 模板清單

所有的 HTML 檔案皆存放於 `app/templates/` 中。

| 模板路徑 | 說明 | 繼承對象 |
| :--- | :--- | :--- |
| `base.html` | 基礎模板，包含共用的 Header、Footer、Flash 訊息，並會根據 Session 中的 `theme_preference` 載入對應的 CSS 或背景圖片。 | (無) |
| `auth/login.html` | 登入表單頁面。 | `base.html` |
| `auth/register.html`| 註冊表單頁面。 | `base.html` |
| `dashboard/index.html`| 顯示總步數、運動歷史列表（搭配皮克敏風格背景）。 | `base.html` |
| `records/new.html` | 填寫游泳距離與時間的輸入表單。 | `base.html` |

---

## 4. 路由骨架程式碼
所有的路由函式骨架已建立於 `app/routes/` 之下，包含 `auth.py`, `dashboard.py`, 與 `record.py`。
# 路由與頁面設計文件 (Routes) - 皮克敏水性類型運動換算步數系統

這份文件規劃了系統中所有的 URL 路由、對應的處理邏輯與渲染的 HTML 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 回傳 | 說明 |
| --- | --- | --- | --- | --- |
| **看板首頁** | GET | `/` | `templates/index.html` | 顯示個人運動成就看板，包含目前步數、背景 |
| **歷史紀錄頁** | GET | `/history` | `templates/history.html` | 顯示過往運動換算紀錄清單 |
| **新增運動數據** | POST | `/api/record` | JSON 回傳 | 接收游泳數據，換算並儲存，回傳最新進度 |
| **切換背景** | POST | `/api/background` | JSON 回傳 | 更新使用者背景設定 |
| **取得最新狀態** | GET | `/api/status` | JSON 回傳 | 取得當前總步數與皮克敏狀態 (供前端重新整理用) |

## 2. 每個路由的詳細說明

### 2.1 `GET /` (看板首頁)
- **輸入**：無。
- **處理邏輯**：
  - 呼叫 `User.get_by_id(1)` 取得使用者資料（MVP 先寫死預設 ID = 1）。
  - 將使用者的目前步數、背景等資料傳入模板。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：若找不到使用者，則建立預設使用者後再渲染。

### 2.2 `GET /history` (歷史紀錄頁)
- **輸入**：無。
- **處理邏輯**：
  - 呼叫 `User.get_by_id(1)` 取得使用者資料。
  - 呼叫 `Record.get_all_by_user(1)` 取得該使用者的所有運動紀錄。
- **輸出**：渲染 `history.html`。
- **錯誤處理**：無紀錄時顯示空狀態提示。

### 2.3 `POST /api/record` (新增運動數據)
- **輸入**：JSON 格式的 payload，包含 `swim_distance_m` (公尺) 與 `swim_time_min` (分鐘)。
- **處理邏輯**：
  - 驗證輸入資料為有效數字。
  - 將游泳數據換算為步數（例如：每 10 公尺 = 30 步，依後續實作公式定）。
  - 呼叫 `Record.create()` 儲存紀錄。
  - 取得舊總步數，加上新增步數後呼叫 `User.update()`。
  - 檢查是否達到新成就門檻，若有則呼叫 `Achievement.create()`。
- **輸出**：回傳 JSON，包含 `{ "success": true, "added_steps": 300, "total_steps": 1500, "new_achievements": [...] }`。
- **錯誤處理**：若輸入不合法，回傳 HTTP 400 與錯誤訊息。

### 2.4 `POST /api/background` (切換背景)
- **輸入**：JSON 格式的 payload，包含 `background_id` (背景名稱)。
- **處理邏輯**：
  - 呼叫 `User.update(current_background=background_id)` 更新資料。
- **輸出**：回傳 JSON `{ "success": true }`。
- **錯誤處理**：若背景 ID 無效，回傳 HTTP 400。

### 2.5 `GET /api/status` (取得最新狀態)
- **輸入**：無。
- **處理邏輯**：
  - 呼叫 `User.get_by_id(1)` 與 `Achievement.get_all_by_user(1)`。
- **輸出**：回傳 JSON `{ "total_steps": 1500, "current_background": "ocean", "achievements": [...] }`。
- **錯誤處理**：若無使用者則回傳 404。

## 3. Jinja2 模板清單

所有的 HTML 頁面皆位於 `app/templates/` 目錄：

1. **`base.html`**
   - **用途**：所有頁面的基底模板 (Base Template)。
   - **內容**：包含 HTML 標頭、匯入共通的 CSS (`style.css`) 與共用的導覽列 (Navbar)。
2. **`index.html`**
   - **用途**：個人運動成就看板主頁。
   - **繼承**：繼承自 `base.html`。
   - **內容**：顯示動態進度條、皮克敏圖示、背景，並包含一個表單或按鈕用來輸入游泳數據 (由 `dashboard.js` 處理 Fetch)。
3. **`history.html`**
   - **用途**：歷史紀錄查詢頁面。
   - **繼承**：繼承自 `base.html`。
   - **內容**：使用 Jinja2 的 `for` 迴圈列表呈現所有過去的運動紀錄。
