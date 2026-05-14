from flask import Blueprint, render_template

page_bp = Blueprint('page', __name__)

@page_bp.route('/')
def index():
    """
    看板首頁路由
    - 取得預設使用者的總步數與設定
    - 渲染 templates/index.html
    """
    pass

@page_bp.route('/history')
def history():
    """
    歷史紀錄頁路由
    - 取得預設使用者的所有運動紀錄
    - 渲染 templates/history.html
    """
    pass
