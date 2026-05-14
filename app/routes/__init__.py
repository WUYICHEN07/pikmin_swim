# 這是 routes 的 __init__.py 檔案
# 未來會在 app.py 中註冊這裡的 Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .record import record_bp
