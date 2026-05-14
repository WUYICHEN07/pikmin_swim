from flask import request, jsonify
from . import api_bp

@api_bp.route('/api/sync', methods=['POST'])
def sync_watch_data():
    """
    (預留) 接收外部運動手錶的 JSON 數據，
    將水上運動距離轉換為步數並儲存。
    """
    pass
