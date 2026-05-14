from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    首頁路由：
    檢查使用者是否已登入，若登入則重導向 /dashboard，否則重導向 /login
    """
    pass

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    個人主控台：
    - 取得目前登入使用者的歷史運動紀錄與換算步數
    - 渲染 templates/dashboard/index.html，並套用使用者偏好的主題背景
    """
    pass

@dashboard_bp.route('/settings/theme', methods=['POST'])
def update_theme():
    """
    更新背景主題設定：
    - 接收表單傳來的 theme_name
    - 呼叫 User Model 更新資料庫
    - 重導向回 /dashboard
    """
    pass
