import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用 dict 方式存取
    return conn

def init_db():
    """初始化資料庫（執行 schema.sql 建表）"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        return
        
    with get_db_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    print("Database initialized successfully.")
