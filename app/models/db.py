import sqlite3
import os

# 確保 instance 資料夾存在
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')

def get_db_connection():
    """取得資料庫連線"""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以用字典方式存取欄位
    return conn

def init_db():
    """初始化資料庫並建立資料表"""
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'pikmin.db')

def get_db_connection():
    """取得 SQLite 資料庫連線，並將回傳結果轉換為字典形式。"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """使用 schema.sql 初始化資料庫"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_script = f.read()
        conn = get_db_connection()
        conn.executescript(schema_script)
        conn.commit()
        conn.close()
