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
