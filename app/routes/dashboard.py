from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from app.models.record import SportsRecord

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    首頁路由：
    檢查使用者是否已登入，若登入則重導向 /dashboard，否則重導向 /login
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    個人主控台：
    - 取得目前登入使用者的歷史運動紀錄與換算步數
    - 渲染 templates/dashboard/index.html，並套用使用者偏好的主題背景
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))

    user = User.get_by_id(user_id)
    records = SportsRecord.get_by_user_id(user_id)
    
    # 計算總步數
    total_steps = sum(record['steps'] for record in records if record['steps'])

    return render_template('dashboard/index.html', user=user, records=records, total_steps=total_steps)

@dashboard_bp.route('/settings/theme', methods=['POST'])
def update_theme():
    """
    更新背景主題設定：
    - 接收表單傳來的 theme_name
    - 呼叫 User Model 更新資料庫
    - 重導向回 /dashboard
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    theme_name = request.form.get('theme_name')
    if theme_name:
        User.update_theme(user_id, theme_name)
        flash('背景主題已更新！', 'success')
    else:
        flash('無效的主題設定。', 'danger')

    return redirect(url_for('dashboard.dashboard'))
