# 路由設計 (Routes Design)

這份文件根據 PRD、架構文件與流程圖，定義了 Pikmin Swim 系統所有的 URL 路由、處理邏輯及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
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
