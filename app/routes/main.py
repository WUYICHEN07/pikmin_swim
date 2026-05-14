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
