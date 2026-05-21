import sqlite3
from . import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash, theme='pool'):
        """建立新使用者"""
import os

DB_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    # Ensure instance folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash, theme) 
                   VALUES (?, ?, ?, ?)''',
                (username, email, password_hash, theme)
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
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
            return None
        finally:
            conn.close()
from .db_helper import get_db_connection
import sqlite3

class User:
    """使用者資料表操作模型"""

    @staticmethod
    def create(username, password_hash, theme_preference='default'):
        """
        新增一筆使用者記錄
        :param username: 使用者帳號
        :param password_hash: 雜湊後的密碼
        :param theme_preference: 背景主題偏好
        :return: 新增的記錄 ID，若失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password_hash, theme_preference) VALUES (?, ?, ?)',
                    (username, password_hash, theme_preference)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in User.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄
        :return: 使用者記錄列表，若失敗則回傳空列表
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in User.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得單一使用者記錄
        :param user_id: 使用者 ID
        :return: 使用者記錄 dict，若找不到或失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        """
        根據帳號取得單一使用者記錄
        :param username: 使用者帳號
        :return: 使用者記錄 dict，若找不到或失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_username: {e}")
            return None

    @staticmethod
    def update_theme(user_id, theme_preference):
        """
        更新使用者的背景主題偏好
        :param user_id: 使用者 ID
        :param theme_preference: 新的主題名稱
        :return: 布林值，代表是否更新成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET theme_preference = ? WHERE id = ?',
                    (theme_preference, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in User.update_theme: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """
        刪除使用者記錄
        :param user_id: 使用者 ID
        :return: 布林值，代表是否刪除成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in User.delete: {e}")
            return False
from .db import get_db_connection

class User:
    @staticmethod
    def create(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user (username) VALUES (?)',
            (username,)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        user = conn.execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        """根據 Email 取得使用者 (用於登入驗證)"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_theme(user_id, theme):
        """更新使用者主題背景"""
        conn = get_db_connection()
        conn.execute('UPDATE users SET theme = ? WHERE id = ?', (theme, user_id))
        conn.commit()
    def update_background(user_id, background):
        conn = get_db_connection()
        conn.execute(
            "UPDATE users SET preferred_background = ? WHERE id = ?",
            (background, user_id)
        )
        conn.commit()
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM user').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, total_steps=None, current_background=None):
        conn = get_db_connection()
        updates = []
        params = []
        if total_steps is not None:
            updates.append('total_steps = ?')
            params.append(total_steps)
        if current_background is not None:
            updates.append('current_background = ?')
            params.append(current_background)
            
        if updates:
            params.append(user_id)
            query = f'UPDATE user SET {", ".join(updates)} WHERE id = ?'
            conn.execute(query, tuple(params))
            conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.execute('DELETE FROM user WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
