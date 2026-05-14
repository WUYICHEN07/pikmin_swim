from .db import get_db_connection

class Achievement:
    @staticmethod
    def create(user_id, name, description):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO achievement (user_id, name, description) 
            VALUES (?, ?, ?)
            ''',
            (user_id, name, description)
        )
        conn.commit()
        achievement_id = cursor.lastrowid
        conn.close()
        return achievement_id

    @staticmethod
    def get_by_id(achievement_id):
        conn = get_db_connection()
        ach = conn.execute(
            'SELECT * FROM achievement WHERE id = ?',
            (achievement_id,)
        ).fetchone()
        conn.close()
        return dict(ach) if ach else None

    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db_connection()
        achievements = conn.execute(
            'SELECT * FROM achievement WHERE user_id = ? ORDER BY unlocked_at DESC',
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(a) for a in achievements]

    @staticmethod
    def delete(achievement_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM achievement WHERE id = ?', (achievement_id,))
        conn.commit()
        conn.close()
