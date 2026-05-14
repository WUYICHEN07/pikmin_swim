-- 建立使用者資料表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    preferred_background TEXT DEFAULT 'default_ocean',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立游泳紀錄資料表
CREATE TABLE IF NOT EXISTS swim_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    swim_duration_minutes REAL,
    stroke_count INTEGER,
    converted_steps INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
