from .db_helper import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash, theme_preference='default'):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, theme_preference) VALUES (?, ?, ?)',
                (username, password_hash, theme_preference)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_username(username):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()

    @staticmethod
    def update_theme(user_id, theme_preference):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET theme_preference = ? WHERE id = ?',
                (theme_preference, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
