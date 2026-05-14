from flask import Blueprint

record_bp = Blueprint('record', __name__)

@record_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    新增紀錄頁面：
    顯示填寫水上運動數據的表單 (templates/records/new.html)
    """
    pass

@record_bp.route('/records', methods=['POST'])
def create_record():
    """
    建立運動紀錄：
    - 接收表單資料 (sport_type, distance_m, duration_min)
    - 寫入 sports_records 資料表
    - 呼叫轉換引擎計算步數
    - 寫入 step_conversions 資料表
    - 重導向至 /dashboard
    """
    pass

@record_bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    刪除運動紀錄：
    - 確認該紀錄是否屬於當前使用者
    - 從資料庫刪除紀錄（串聯刪除轉換紀錄）
    - 重導向至 /dashboard
    """
    pass
