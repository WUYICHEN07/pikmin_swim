# app/models/__init__.py
import sqlite3
import os

def get_db_connection():
    """取得資料庫連線的共用方法"""
    # 預設資料庫路徑設在專案根目錄的 instance/database.db
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    # 將回傳結果設為 dict 格式，方便用欄位名稱存取
    conn.row_factory = sqlite3.Row
    return conn
