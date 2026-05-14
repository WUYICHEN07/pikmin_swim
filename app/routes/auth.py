from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染 login.html
    POST: 接收 username, password，驗證密碼，成功則寫入 session 並重導向 /
    """
    pass
    處理使用者登入：
    - GET: 顯示登入表單 (templates/auth/login.html)
    - POST: 接收表單資料，驗證 User，設定 session，重導向至 /dashboard
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫帳號與密碼！', 'danger')
            return render_template('auth/login.html')

        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('登入成功！', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('帳號或密碼錯誤。', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染 register.html
    POST: 接收 username, password，雜湊密碼後存入 DB，重導向 /login
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出。
    邏輯：清除 session 中的 user_id
    輸出：重導向至 /login
    """
    pass
    處理使用者註冊：
    - GET: 顯示註冊表單 (templates/auth/register.html)
    - POST: 接收表單資料，建立 User，重導向至 /login
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫帳號與密碼！', 'danger')
            return render_template('auth/register.html')

        existing_user = User.get_by_username(username)
        if existing_user:
            flash('這個帳號已經被註冊過囉！', 'danger')
            return render_template('auth/register.html')

        # 密碼加密
        password_hash = generate_password_hash(password)
        User.create(username, password_hash)
        
        flash('註冊成功！請登入。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理使用者登出：
    清除 session 資料，重導向至 /login
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('auth.login'))
