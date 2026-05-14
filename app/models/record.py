from .db_helper import get_db_connection

class SportsRecord:
    @staticmethod
    def create(user_id, sport_type, distance_m, duration_min):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO sports_records (user_id, sport_type, distance_m, duration_min) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, sport_type, distance_m, duration_min)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(record_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sports_records WHERE id = ?', (record_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_user_id(user_id):
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

    @staticmethod
    def update(record_id, sport_type, distance_m, duration_min):
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

    @staticmethod
    def delete(record_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sports_records WHERE id = ?', (record_id,))
            conn.commit()
            return cursor.rowcount > 0
