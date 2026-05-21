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
from .user import User, get_db_connection
from .swim_record import SwimRecord
# 這是 models 的 __init__.py 檔案
from .user import User
from .record import SportsRecord
from .conversion import StepConversion
from .db_helper import init_db, get_db_connection
from .db import get_db_connection, init_db
from .user import User
from .record import Record
from .achievement import Achievement

__all__ = ['get_db_connection', 'init_db', 'User', 'Record', 'Achievement']
