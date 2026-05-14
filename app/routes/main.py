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
    """
    pass
