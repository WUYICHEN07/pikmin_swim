from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染 login.html
    POST: 接收 username, password，驗證密碼，成功則寫入 session 並重導向 /
    """
    pass

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
