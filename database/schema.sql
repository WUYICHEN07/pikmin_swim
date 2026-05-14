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
-- schema.sql: 建立 SQLite 資料庫結構的 SQL 語法

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    total_steps INTEGER DEFAULT 0,
    current_background TEXT DEFAULT 'default',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    swim_distance_m REAL NOT NULL,
    swim_time_min REAL NOT NULL,
    converted_steps INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS achievement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- 初始化一個預設使用者 (作為 MVP 單一使用者測試用)
INSERT INTO user (username, total_steps, current_background) 
SELECT 'TestUser', 0, 'default' 
WHERE NOT EXISTS (SELECT 1 FROM user WHERE id = 1);
