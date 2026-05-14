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
