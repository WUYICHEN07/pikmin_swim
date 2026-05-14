from .db import get_db_connection

class User:
    @staticmethod
    def create(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user (username) VALUES (?)',
            (username,)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM user').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, total_steps=None, current_background=None):
        conn = get_db_connection()
        updates = []
        params = []
        if total_steps is not None:
            updates.append('total_steps = ?')
            params.append(total_steps)
        if current_background is not None:
            updates.append('current_background = ?')
            params.append(current_background)
            
        if updates:
            params.append(user_id)
            query = f'UPDATE user SET {", ".join(updates)} WHERE id = ?'
            conn.execute(query, tuple(params))
            conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM user WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
