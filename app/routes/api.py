from flask import request, jsonify
from . import api_bp
from app.models.activity import Activity
from app.models.user import User

@api_bp.route('/api/sync', methods=['POST'])
def sync_watch_data():
    """
    (預留) 接收外部運動手錶的 JSON 數據，
    將水上運動距離轉換為步數並儲存。
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400
        
    user_id = data.get('user_id')
    sport_type = data.get('sport_type')
    duration = data.get('duration')
    
    if not all([user_id, sport_type, duration]):
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        duration = int(duration)
        steps_earned = duration * 100
        
        activity_data = {
            'user_id': user_id,
            'sport_type': sport_type,
            'distance': data.get('distance', 0.0),
            'duration': duration,
            'steps_earned': steps_earned
        }
        Activity.create(activity_data)
        
        user = User.get_by_id(user_id)
        if user:
            User.update(user_id, {'total_steps': user['total_steps'] + steps_earned})
            
        return jsonify({
            "status": "success", 
            "steps_earned": steps_earned,
            "message": "Data synchronized successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from ..models.activity import Activity

@api_bp.route('/activity', methods=['POST'])
def create_activity():
    """
    [F-01] 運動數據接入 API
    接收穿戴裝置傳來的 JSON 運動數據，包含:
    - user_id (int)
    - activity_type (str)
    - duration_minutes (int)
    - distance_meters (float, optional)
    - heart_rate_avg (int, optional)
    
    預期回傳：
    - 成功: 201 Created, 回傳轉換後的步數
    - 失敗: 400 Bad Request (資料格式錯誤或缺漏)
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/record', methods=['POST'])
def add_record():
    """
    新增運動數據 API
    - 接收 JSON 格式的 swim_distance_m 與 swim_time_min
    - 進行步數換算邏輯
    - 儲存至 Record 與更新 User 總步數
    - 檢查是否解鎖新成就
    - 回傳最新狀態與解鎖資訊的 JSON
    """
    pass

@api_bp.route('/background', methods=['POST'])
def update_background():
    """
    切換背景 API
    - 接收 JSON 格式的 background_id
    - 更新使用者的 current_background
    - 回傳成功或失敗的 JSON
    """
    pass

@api_bp.route('/status', methods=['GET'])
def get_status():
    """
    取得最新狀態 API
    - 取得使用者的當前步數、背景與解鎖成就
    - 回傳 JSON 供前端非同步更新畫面
    """
    pass
