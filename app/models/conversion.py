from .db_helper import get_db_connection

class StepConversion:
    @staticmethod
    def create(sports_record_id, steps):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO step_conversions (sports_record_id, steps) VALUES (?, ?)',
                (sports_record_id, steps)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(conversion_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM step_conversions WHERE id = ?', (conversion_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_record_id(sports_record_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM step_conversions WHERE sports_record_id = ?', (sports_record_id,))
            return cursor.fetchone()

    @staticmethod
    def update(conversion_id, steps):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE step_conversions SET steps = ? WHERE id = ?',
                (steps, conversion_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(conversion_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM step_conversions WHERE id = ?', (conversion_id,))
            conn.commit()
            return cursor.rowcount > 0
