from flask import render_template, request, redirect, url_for, session, flash
from . import main_bp
from app.models.user import User
from app.models.activity import Activity

@main_bp.route('/')
def index():
    """首頁與登入頁面"""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/login', methods=['POST'])
def login():
    """處理使用者登入"""
    username = request.form.get('username')
    if not username:
        flash('請輸入玩家名稱', 'danger')
        return redirect(url_for('main.index'))
        
    user = User.get_by_username(username)
    if not user:
        user_id = User.create({'username': username})
        flash(f'歡迎新玩家 {username}！', 'success')
    else:
        user_id = user['id']
        flash(f'歡迎回來，{username}！', 'success')
        
    session['user_id'] = user_id
    return redirect(url_for('main.dashboard'))

@main_bp.route('/logout', methods=['POST'])
def logout():
    """處理使用者登出"""
    session.pop('user_id', None)
    flash('你已經成功登出。', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
def dashboard():
    """運動儀表板，顯示總步數與水下皮克敏背景"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
        
    user = User.get_by_id(user_id)
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('main.index'))
        
    return render_template('dashboard.html', user=user)

@main_bp.route('/record')
def record_page():
    """顯示新增水上運動數據的表單頁面"""
    if 'user_id' not in session:
        return redirect(url_for('main.index'))
    return render_template('record.html')

@main_bp.route('/record', methods=['POST'])
def create_record():
    """接收表單數據，計算步數並寫入資料庫"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
        
    sport_type = request.form.get('sport_type')
    distance = request.form.get('distance')
    duration = request.form.get('duration')
    
    if not sport_type or not duration:
        flash('請填寫必要的運動資訊！', 'danger')
        return redirect(url_for('main.record_page'))
        
    try:
        duration = int(duration)
        distance = float(distance) if distance else 0.0
    except ValueError:
        flash('時間與距離必須為數字！', 'danger')
        return redirect(url_for('main.record_page'))
        
    # 簡單的步數換算邏輯：每分鐘游泳 100 步
    steps_earned = duration * 100
    
    data = {
        'user_id': user_id,
        'sport_type': sport_type,
        'distance': distance,
        'duration': duration,
        'steps_earned': steps_earned
    }
    
    # 儲存紀錄
    Activity.create(data)
    
    # 更新使用者步數
    user = User.get_by_id(user_id)
    User.update(user_id, {'total_steps': user['total_steps'] + steps_earned})
    
    flash(f'太棒了！本次運動為你轉換了 {steps_earned} 步！', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/history')
def history():
    """顯示歷史運動紀錄"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
        
    activities = Activity.get_by_user_id(user_id)
    return render_template('history.html', activities=activities)

@main_bp.route('/settings/background', methods=['POST'])
def update_background():
    """更新使用者的水下背景主題"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))
        
    bg_theme = request.form.get('background_theme')
    if bg_theme:
        User.update(user_id, {'current_background': bg_theme})
        flash('背景主題已成功更新！', 'success')
        
    return redirect(url_for('main.dashboard'))
from flask import render_template, request, redirect, url_for, session
from . import main_bp
from ..models.user import User
from ..models.activity import Activity

@main_bp.route('/')
def dashboard():
    """
    [F-03] 系統首頁 / 個人數據總覽
    顯示目前的個人累積步數與運動歷史紀錄。
    預期邏輯：
    - 檢查 user_id 是否在 session 中，沒有則重導向到 login
    - 取得總步數與最近的活動紀錄
    - 渲染 dashboard.html
    """
    pass

@main_bp.route('/settings/theme', methods=['POST'])
def update_theme():
    """
    [F-04] 切換背景主題
    接收表單傳來的 theme 參數，更新至資料庫。
    預期邏輯：
    - 更新 User 紀錄
    - 重導向回 dashboard
from flask import Blueprint, render_template, session, redirect, url_for, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁與儀表板的請求。
    輸入：無
    邏輯：確認登入狀態，獲取總累積步數及使用者偏好背景
    輸出：渲染 index.html 或重導向 /login
    """
    pass

@main_bp.route('/history')
def history():
    """
    檢視歷史轉換紀錄。
    輸入：無
    邏輯：讀取該使用者的所有 swim_records
    輸出：渲染 history.html
    """
    pass

@main_bp.route('/background', methods=['POST'])
def change_background():
    """
    更換使用者背景設定。
    輸入：表單欄位 bg_choice
    邏輯：更新使用者的 preferred_background 欄位
    輸出：重導向回首頁 /
    """
    pass
