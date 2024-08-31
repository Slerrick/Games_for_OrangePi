import psutil
def check_cpu():
    cpu_percent = psutil.cpu_percent(interval=1)  # Получаем среднюю загрузку CPU за 1 секунду
    print(f"Загрузка CPU: {cpu_percent}%")

    # Получаем загрузку каждого ядра
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    print(f"Загрузка ядер: {cpu_per_core}")
def check_disk():
    disk_percent = psutil.disk_usage(path="C:")
    print(f"Загрузка диска: {disk_percent}%")