from .db_helper import get_db_connection
import sqlite3

class StepConversion:
    """步數轉換紀錄資料表操作模型"""

    @staticmethod
    def create(sports_record_id, steps):
        """
        新增一筆步數轉換記錄
        :param sports_record_id: 關聯的運動記錄 ID
        :param steps: 換算後的步數
        :return: 新增的記錄 ID，若失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO step_conversions (sports_record_id, steps) VALUES (?, ?)',
                    (sports_record_id, steps)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得系統內所有步數轉換記錄
        :return: 記錄列表，若失敗則回傳空列表
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM step_conversions ORDER BY created_at DESC')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(conversion_id):
        """
        根據 ID 取得單一步數轉換記錄
        :param conversion_id: 記錄 ID
        :return: 記錄 dict，若找不到或失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM step_conversions WHERE id = ?', (conversion_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_record_id(sports_record_id):
        """
        根據運動記錄 ID 取得對應的步數轉換記錄
        :param sports_record_id: 關聯的運動記錄 ID
        :return: 記錄 dict
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM step_conversions WHERE sports_record_id = ?', (sports_record_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.get_by_record_id: {e}")
            return None

    @staticmethod
    def update(conversion_id, steps):
        """
        更新步數轉換記錄
        :param conversion_id: 記錄 ID
        :param steps: 新的步數
        :return: 布林值，代表是否更新成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE step_conversions SET steps = ? WHERE id = ?',
                    (steps, conversion_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.update: {e}")
            return False

    @staticmethod
    def delete(conversion_id):
        """
        刪除步數轉換記錄
        :param conversion_id: 記錄 ID
        :return: 布林值，代表是否刪除成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM step_conversions WHERE id = ?', (conversion_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in StepConversion.delete: {e}")
            return False
