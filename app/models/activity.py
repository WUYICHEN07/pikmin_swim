import sqlite3
from .db import get_db_connection

class Activity:
    @staticmethod
    def create(data):
        """新增一筆運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO activities (user_id, sport_type, distance, duration, steps_earned)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (data.get('user_id'), data.get('sport_type'), data.get('distance', 0.0), 
                 data.get('duration'), data.get('steps_earned'))
            )
            conn.commit()
            activity_id = cursor.lastrowid
            return activity_id
        except sqlite3.Error as e:
            print(f"Error creating activity: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            activities = conn.execute('SELECT * FROM activities ORDER BY created_at DESC').fetchall()
            return activities
        except sqlite3.Error as e:
            print(f"Error getting all activities: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            activity = conn.execute('SELECT * FROM activities WHERE id = ?', (id,)).fetchone()
            return activity
        except sqlite3.Error as e:
            print(f"Error getting activity by id: {e}")
            return None
        finally:
            if conn:
                conn.close()
                
    @staticmethod
    def get_by_user_id(user_id):
        """取得特定使用者的所有運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            activities = conn.execute(
                'SELECT * FROM activities WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            ).fetchall()
            return activities
        except sqlite3.Error as e:
            print(f"Error getting activities by user_id: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(id, data):
        """更新單筆運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            fields = []
            values = []
            for key, value in data.items():
                fields.append(f"{key} = ?")
                values.append(value)
            
            if not fields:
                return False
                
            values.append(id)
            query = f"UPDATE activities SET {', '.join(fields)} WHERE id = ?"
            
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating activity: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(id):
        """刪除單筆運動記錄"""
        conn = None
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM activities WHERE id = ?', (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting activity: {e}")
            return False
        finally:
            if conn:
                conn.close()
