from flask import Blueprint, render_template, request, redirect, url_for, session, flash

convert_bp = Blueprint('convert', __name__)

@convert_bp.route('/convert', methods=['GET', 'POST'])
def convert_steps():
    """
    處理游泳數據轉步數的功能。
    GET: 渲染 convert.html 表單
    POST: 接收 swim_duration 或 stroke_count，呼叫轉換演算法，將步數存入 DB
    輸出: 成功後 flash 提示並重導向 /
    """
    pass
