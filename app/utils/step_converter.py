def calculate_steps(sport_type, distance_m, duration_min):
    """
    步數轉換引擎：
    根據運動類型、距離與時間，計算出等效的步數。
    這裡採用簡單的基礎邏輯，未來可擴充針對不同泳姿套用不同權重。
    
    :param sport_type: 運動類型（例如：'freestyle', 'breaststroke' 等）
    :param distance_m: 游泳距離（公尺）
    :param duration_min: 運動時間（分鐘）
    :return: 換算後的步數（整數）
    """
    # 基礎轉換：每 1 公尺游泳相當於 10 步 (只是範例數字，可依需求調整)
    # 也可以把時間納入考量，例如每 1 分鐘加成 20 步
    
    base_steps_per_meter = 10
    steps_per_minute = 20
    
    # 假設自由式有額外的強度加成 1.2 倍
    multiplier = 1.0
    if sport_type == 'freestyle':
        multiplier = 1.2
    elif sport_type == 'butterfly':
        multiplier = 1.5

    total_steps = (distance_m * base_steps_per_meter + duration_min * steps_per_minute) * multiplier
    
    return int(total_steps)
