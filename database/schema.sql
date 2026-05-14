-- database/schema.sql

-- 建立 Users 資料表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    theme TEXT DEFAULT 'pool',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立 Activities 資料表
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    distance_meters REAL,
    heart_rate_avg INTEGER,
    converted_steps INTEGER NOT NULL,
    recorded_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
