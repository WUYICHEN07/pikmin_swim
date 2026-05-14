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
