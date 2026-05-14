# 路由設計：皮克敏水性類型運動換算步數系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
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
