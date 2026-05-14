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
