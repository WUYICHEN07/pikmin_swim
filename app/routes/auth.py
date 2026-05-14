from flask import render_template, request, redirect, url_for, session
from . import auth_bp
from ..models.user import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    [F-05] 處理使用者登入驗證
    - GET: 渲染 login.html
    - POST: 驗證帳號密碼，成功後寫入 session，重導向首頁
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    [F-05] 使用者註冊頁面
    - GET: 渲染 register.html
    - POST: 接收註冊資料，建立帳號後重導向至登入頁
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    [F-05] 使用者登出
    清除 session 資料，重導向至登入頁
    """
    pass
