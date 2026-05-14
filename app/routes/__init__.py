from flask import Blueprint

# 初始化 Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# 引入路由以便註冊 (避免循環依賴，通常在檔案底部引入)
from . import main, api
