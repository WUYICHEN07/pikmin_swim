from flask import Blueprint

# 初始化 Blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# 引入路由以便註冊 (這裡放到底部避免 circular import)
from . import api, main, auth
