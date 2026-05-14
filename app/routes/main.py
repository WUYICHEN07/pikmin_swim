from flask import render_template, request, redirect, url_for, session
from . import main_bp

@main_bp.route('/')
def index():
    """首頁與登入頁面"""
    pass

@main_bp.route('/login', methods=['POST'])
def login():
    """處理使用者登入"""
    pass

@main_bp.route('/dashboard')
def dashboard():
    """運動儀表板，顯示總步數與水下皮克敏背景"""
    pass

@main_bp.route('/record')
def record_page():
    """顯示新增水上運動數據的表單頁面"""
    pass

@main_bp.route('/record', methods=['POST'])
def create_record():
    """接收表單數據，計算步數並寫入資料庫"""
    pass

@main_bp.route('/history')
def history():
    """顯示歷史運動紀錄"""
    pass

@main_bp.route('/settings/background', methods=['POST'])
def update_background():
    """更新使用者的水下背景主題"""
    pass
