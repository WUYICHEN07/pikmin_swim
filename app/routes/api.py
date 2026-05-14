from flask import request, jsonify
from . import api_bp
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
    """
    pass
