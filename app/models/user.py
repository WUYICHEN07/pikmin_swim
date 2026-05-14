import sqlite3
from . import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash, theme='pool'):
        """建立新使用者"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash, theme) 
                   VALUES (?, ?, ?, ?)''',
                (username, email, password_hash, theme)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email 已存在的例外處理
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得使用者"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        """根據 Email 取得使用者 (用於登入驗證)"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_theme(user_id, theme):
        """更新使用者主題背景"""
        conn = get_db_connection()
        conn.execute('UPDATE users SET theme = ? WHERE id = ?', (theme, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
