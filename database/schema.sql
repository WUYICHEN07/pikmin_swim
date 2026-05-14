-- schema.sql
-- 皮克敏水性類型運動換算步數系統 SQLite 建表語法

-- 建立 users 表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    total_steps INTEGER DEFAULT 0 NOT NULL,
    current_background TEXT DEFAULT 'ocean_default',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立 activities 表
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sport_type TEXT NOT NULL,
    distance REAL DEFAULT 0,
    duration INTEGER NOT NULL,  -- 以分鐘為單位
    steps_earned INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
