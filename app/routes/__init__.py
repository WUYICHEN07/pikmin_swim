from flask import Blueprint, render_template, request, redirect, url_for, session

# 此檔案目前僅供初始化模組使用，可由 app.py 匯入 Blueprint
# 這是 routes 的 __init__.py 檔案
# 未來會在 app.py 中註冊這裡的 Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .record import record_bp
from .page import page_bp
from .api import api_bp

__all__ = ['page_bp', 'api_bp']
