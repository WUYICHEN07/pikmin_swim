-- 建立使用者資料表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    theme_preference TEXT DEFAULT 'default',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立運動紀錄資料表
CREATE TABLE IF NOT EXISTS sports_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sport_type TEXT NOT NULL,
    distance_m REAL,
    duration_min REAL,
    record_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 建立步數轉換紀錄資料表
CREATE TABLE IF NOT EXISTS step_conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sports_record_id INTEGER NOT NULL,
    steps INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sports_record_id) REFERENCES sports_records(id) ON DELETE CASCADE
);
