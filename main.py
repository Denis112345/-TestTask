import tkinter as tk
from UI.main_ui import LoadAnalyzerUI
from database_requesting.database_handlers import create_tables_if_not_exist


def main():
    """
        Функция которая запускает весь проект
    """
    create_tables_if_not_exist() # Инциализация таблицы в БД если её нет
    window = tk.Tk()
    UI = LoadAnalyzerUI(window)
    UI.run() # Запуск графиического интерфейса

if __name__ == '__main__':
    main()