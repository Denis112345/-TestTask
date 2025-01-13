import psutil # Библиотека для сканирования системы

class SystemMonitor:
    """
    Класс для мониторинга ресурсов системы (CPU, RAM, ROM)
    """

    def __init__(self):
        """
        Инициализация класса
        """
        pass

    @staticmethod
    def get_system_resorces(interval=1) -> dict[str, str]:
        """
        Метод получения данных нагрузки системы

        Args:
            interval: интервал для получения данных нагрузки процессора

        """
        cpu_percent = psutil.cpu_percent(interval) # Загрузка CPU (процент), интервал 1 секунда

        ram = psutil.virtual_memory()  # Информация об оперативной памяти
        ram_total = round(ram.total / (1024 ** 3), 1)  # RAM в гигабайтах
        ram_free = round(ram.available / (1024 ** 3), 1)  # Свободная оперативная память в гигабайтах

        disk = psutil.disk_usage('/')  # Информация о диске, / - корень
        disk_total = round(disk.total / (1024 ** 3), 1)  # Объем диска в гигабайтах
        disk_free = round(disk.free / (1024 ** 3), 1) # Свободное дисковое пространство в гигабайтах

        return {
            'CPU': str(cpu_percent) + '%',
            'RAM': str(ram_free) + ' ГБ / ' + str(ram_total) + ' ГБ',
            'ROM': str(disk_free) + ' ГБ / ' + str(disk_total) + ' ГБ',
        }
    
if __name__ == '__main__':
    sys_monitor = SystemMonitor()
    print(sys_monitor.get_system_resorces())