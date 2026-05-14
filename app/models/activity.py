from .db import get_db_connection

class Activity:
    @staticmethod
    def create(user_id, sport_type, distance, duration, steps_earned):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO activities (user_id, sport_type, distance, duration, steps_earned)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (user_id, sport_type, distance, duration, steps_earned)
        )
        conn.commit()
        activity_id = cursor.lastrowid
        conn.close()
        return activity_id

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        activities = conn.execute(
            'SELECT * FROM activities WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
        conn.close()
        return activities
