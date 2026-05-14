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
