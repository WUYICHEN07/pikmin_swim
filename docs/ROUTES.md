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
