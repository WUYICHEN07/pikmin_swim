# 路由設計文件 (API Design)：皮克敏水性類型運動換算步數系統

這份文件規劃了 Flask 應用程式中所有的 URL 路由、對應的 Jinja2 模板，以及外部 API 串接端點。

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
