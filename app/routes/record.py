from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.record import SportsRecord
from app.models.conversion import StepConversion
from app.utils.step_converter import calculate_steps

record_bp = Blueprint('record', __name__)

@record_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    新增紀錄頁面：
    顯示填寫水上運動數據的表單 (templates/records/new.html)
    """
    if 'user_id' not in session:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))
        
    return render_template('records/new.html')

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
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    sport_type = request.form.get('sport_type')
    distance_m = request.form.get('distance_m', type=float)
    duration_min = request.form.get('duration_min', type=float)

    if not sport_type or distance_m is None or duration_min is None:
        flash('請填寫所有欄位且格式須正確！', 'danger')
        return redirect(url_for('record.new_record'))

    # 1. 計算步數
    steps = calculate_steps(sport_type, distance_m, duration_min)

    # 2. 存入運動紀錄
    record_id = SportsRecord.create(user_id, sport_type, distance_m, duration_min)
    
    if record_id:
        # 3. 存入轉換紀錄
        StepConversion.create(record_id, steps)
        flash(f'紀錄新增成功！獲得了 {steps} 步！', 'success')
    else:
        flash('新增紀錄失敗，請稍後再試。', 'danger')

    return redirect(url_for('dashboard.dashboard'))

@record_bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    刪除運動紀錄：
    - 確認該紀錄是否屬於當前使用者
    - 從資料庫刪除紀錄（串聯刪除轉換紀錄）
    - 重導向至 /dashboard
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # 驗證該紀錄是否屬於該使用者
    record = SportsRecord.get_by_id(record_id)
    if not record or record['user_id'] != user_id:
        flash('找不到該紀錄，或您無權刪除。', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    success = SportsRecord.delete(record_id)
    if success:
        flash('紀錄已刪除。', 'success')
    else:
        flash('刪除失敗。', 'danger')

    return redirect(url_for('dashboard.dashboard'))
