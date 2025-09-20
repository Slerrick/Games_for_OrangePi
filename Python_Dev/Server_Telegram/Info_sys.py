import psutil
from typing import Dict, Any

def check_cpu() -> Dict[str, Any]:
    """Проверка загрузки CPU"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        result = {
            'total': cpu_percent,
            'per_core': cpu_per_core,
            'cores': len(cpu_per_core)
        }
        
        print(f"Загрузка CPU: {cpu_percent}%")
        print(f"Загрузка ядер: {cpu_per_core}")
        
        return result
        
    except Exception as e:
        print(f"Ошибка при проверке CPU: {e}")
        return {}

def check_disk(path: str = "C:") -> Dict[str, Any]:
    """Проверка использования диска"""
    try:
        disk_usage = psutil.disk_usage(path)
        
        result = {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent
        }
        
        print(f"Использование диска {path}: {disk_usage.percent}%")
        print(f"Свободно: {disk_usage.free / (1024**3):.2f} GB")
        
        return result
        
    except Exception as e:
        print(f"Ошибка при проверке диска: {e}")
        return {}

def check_memory() -> Dict[str, Any]:
    """Проверка использования памяти"""
    try:
        memory = psutil.virtual_memory()
        
        result = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        }
        
        print(f"Использование памяти: {memory.percent}%")
        print(f"Доступно: {memory.available / (1024**3):.2f} GB")
        
        return result
        
    except Exception as e:
        print(f"Ошибка при проверке памяти: {e}")
        return {}