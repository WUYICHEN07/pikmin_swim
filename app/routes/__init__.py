# 這是 routes 的 __init__.py 檔案
# 未來會在 app.py 中註冊這裡的 Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .record import record_bp
from .page import page_bp
from .api import api_bp

__all__ = ['page_bp', 'api_bp']
