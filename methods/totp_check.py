import time

def time_to_live(secret, interval=30):
    # Получаем текущее время в секундах с момента начала эпохи (Unix timestamp)
    current_time = time.time()
    
    # Вычисляем время жизни текущего кода
    time_elapsed = current_time % interval
    time_remaining = interval - time_elapsed
    
    return time_remaining