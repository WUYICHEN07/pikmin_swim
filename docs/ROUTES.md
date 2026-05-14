# 路由設計 (API Design)

本文件根據 PRD、系統架構與資料庫設計，詳細規劃了系統的所有 URL 路由、對應的處理邏輯與渲染的 HTML 模板。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
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
