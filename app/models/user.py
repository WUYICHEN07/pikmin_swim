import sqlite3
from .db import get_db_connection

class User:
    @staticmethod
    def create(data):
        """新增一筆使用者記錄"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, total_steps, current_background) VALUES (?, ?, ?)',
                (data.get('username'), data.get('total_steps', 0), data.get('current_background', 'ocean_default'))
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有使用者記錄"""
        conn = None
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            return users
        except sqlite3.Error as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆使用者記錄"""
        conn = None
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_username(username):
        """透過使用者名稱取得記錄"""
        conn = None
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Error getting user by username: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(id, data):
        """更新單筆使用者記錄"""
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
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(id):
        """刪除單筆使用者記錄"""
        conn = None
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            if conn:
                conn.close()
