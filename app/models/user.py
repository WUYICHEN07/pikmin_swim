import sqlite3
from .db import get_db_connection

class User:
    @staticmethod
    def create(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Username already exists
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def update_steps(user_id, added_steps):
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET total_steps = total_steps + ? WHERE id = ?',
            (added_steps, user_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_background(user_id, background):
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET current_background = ? WHERE id = ?',
            (background, user_id)
        )
        conn.commit()
        conn.close()
