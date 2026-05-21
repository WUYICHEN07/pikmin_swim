from .db_helper import get_db_connection
import sqlite3

class SportsRecord:
    """水上運動紀錄資料表操作模型"""

    @staticmethod
    def create(user_id, sport_type, distance_m, duration_min):
        """
        新增一筆運動記錄
        :param user_id: 使用者 ID
        :param sport_type: 運動類型
        :param distance_m: 運動距離
        :param duration_min: 運動時間
        :return: 新增的記錄 ID，若失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO sports_records (user_id, sport_type, distance_m, duration_min) 
                       VALUES (?, ?, ?, ?)''',
                    (user_id, sport_type, distance_m, duration_min)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.create: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得系統內所有運動記錄
        :return: 記錄列表，若失敗則回傳空列表
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM sports_records ORDER BY record_date DESC')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(record_id):
        """
        根據 ID 取得單一運動記錄
        :param record_id: 記錄 ID
        :return: 記錄 dict，若找不到或失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM sports_records WHERE id = ?', (record_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得特定使用者的所有運動記錄與轉換的步數
        :param user_id: 使用者 ID
        :return: 記錄列表
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # 同時 Join 步數轉換表，方便前端一次顯示完整資訊
                cursor.execute('''
                    SELECT sr.*, sc.steps 
                    FROM sports_records sr
                    LEFT JOIN step_conversions sc ON sr.id = sc.sports_record_id
                    WHERE sr.user_id = ?
                    ORDER BY sr.record_date DESC
                ''', (user_id,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.get_by_user_id: {e}")
            return []

    @staticmethod
    def update(record_id, sport_type, distance_m, duration_min):
        """
        更新運動記錄
        :param record_id: 記錄 ID
        :param sport_type: 運動類型
        :param distance_m: 運動距離
        :param duration_min: 運動時間
        :return: 布林值，代表是否更新成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''UPDATE sports_records 
                       SET sport_type = ?, distance_m = ?, duration_min = ? 
                       WHERE id = ?''',
                    (sport_type, distance_m, duration_min, record_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.update: {e}")
            return False

    @staticmethod
    def delete(record_id):
        """
        刪除運動記錄
        :param record_id: 記錄 ID
        :return: 布林值，代表是否刪除成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM sports_records WHERE id = ?', (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in SportsRecord.delete: {e}")
            return False
from .db import get_db_connection

class Record:
    @staticmethod
    def create(user_id, swim_distance_m, swim_time_min, converted_steps):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO record (user_id, swim_distance_m, swim_time_min, converted_steps) 
            VALUES (?, ?, ?, ?)
            ''',
            (user_id, swim_distance_m, swim_time_min, converted_steps)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute(
            'SELECT * FROM record WHERE id = ?',
            (record_id,)
        ).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db_connection()
        records = conn.execute(
            'SELECT * FROM record WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def update(record_id, swim_distance_m, swim_time_min, converted_steps):
        conn = get_db_connection()
        conn.execute(
            '''
            UPDATE record SET 
                swim_distance_m = ?, 
                swim_time_min = ?, 
                converted_steps = ? 
            WHERE id = ?
            ''',
            (swim_distance_m, swim_time_min, converted_steps, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM record WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
