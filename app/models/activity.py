from datetime import datetime
from . import get_db_connection

class Activity:
    @staticmethod
    def calculate_steps(activity_type, duration_minutes, distance_meters=None, heart_rate_avg=None):
        """
        水上運動步數換算邏輯 (F-02)
        這裡是一個簡單的模擬換算公式，可依需求調整。
        """
        base_steps_per_minute = 0
        if activity_type == 'swimming':
            base_steps_per_minute = 100  # 游泳每分鐘約等同於 100 步
        elif activity_type == 'water_polo':
            base_steps_per_minute = 120  # 水球運動量大
        elif activity_type == 'diving':
            base_steps_per_minute = 60
        else:
            base_steps_per_minute = 80   # 預設水上運動

        steps = duration_minutes * base_steps_per_minute
        
        # 若有距離數據，微調步數加成
        if distance_meters:
            steps += int(distance_meters * 0.5)
            
        return steps

    @staticmethod
    def create(user_id, activity_type, duration_minutes, recorded_at, distance_meters=None, heart_rate_avg=None):
        """建立新的運動紀錄，並自動換算步數"""
        converted_steps = Activity.calculate_steps(
            activity_type, duration_minutes, distance_meters, heart_rate_avg
        )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO activities 
               (user_id, activity_type, duration_minutes, distance_meters, heart_rate_avg, converted_steps, recorded_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user_id, activity_type, duration_minutes, distance_meters, heart_rate_avg, converted_steps, recorded_at)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id, converted_steps

    @staticmethod
    def get_by_user(user_id, limit=20):
        """取得特定使用者的運動紀錄列表"""
        conn = get_db_connection()
        records = conn.execute(
            'SELECT * FROM activities WHERE user_id = ? ORDER BY recorded_at DESC LIMIT ?', 
            (user_id, limit)
        ).fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_total_steps_by_user(user_id):
        """取得特定使用者的總累積步數"""
        conn = get_db_connection()
        result = conn.execute(
            'SELECT SUM(converted_steps) as total_steps FROM activities WHERE user_id = ?', 
            (user_id,)
        ).fetchone()
        conn.close()
        return result['total_steps'] if result['total_steps'] else 0
