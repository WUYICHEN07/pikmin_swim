import sqlite3
from .user import get_db_connection

class SwimRecord:
    @staticmethod
    def create(user_id, swim_duration_minutes, stroke_count, converted_steps):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO swim_records (user_id, swim_duration_minutes, stroke_count, converted_steps)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, swim_duration_minutes, stroke_count, converted_steps)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute("SELECT * FROM swim_records WHERE id = ?", (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db_connection()
        records = conn.execute(
            "SELECT * FROM swim_records WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_total_steps_by_user(user_id):
        conn = get_db_connection()
        result = conn.execute(
            "SELECT SUM(converted_steps) as total FROM swim_records WHERE user_id = ?", 
            (user_id,)
        ).fetchone()
        conn.close()
        return result['total'] if result['total'] else 0

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM swim_records WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
