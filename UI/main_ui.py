import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading

from data_processing.main_data_processing import SystemMonitor

class LoadAnalyzerUI:
    def __init__(self, window:tk.Tk):
        """

        Инициализация класса

        Args:
            window: Главное окно Tkinter

        """

        self._window = window
        self._window.title('Load Analyzer')
        self._window.geometry('400x300')

        self.auto_update_flag = True

        self._main_frame = ttk.Frame(self._window, padding=(20,20)) # Фрейм для отступа 20 пикселей со всех сторон
        self._main_frame.pack(fill="both", expand=True)

        self._statistic_parametrs = {} # Список всех отслеживаемых значений

        self._create_widgets(['CPU', 'RAM', 'ROM'])

        self.update_thread = threading.Thread(target=self._set_statistic_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def _start_recording(self):
        interval = self._interval_entry.get()
        try:
            interval = int(interval)
        except:
            self._show_error_window('Значние интревала должно быть цифрой или числом')
    
    def _set_statistic_loop(self):
        interval = self._interval_entry.get()
        try:
            interval = int(interval)
        except:
            interval = 1

        while self.auto_update_flag:
            system_statistics = SystemMonitor.get_system_resorces(interval=interval)

            for statistic_key, statistic_value in system_statistics.items():
                print(statistic_key)
                self._set_statistic_value(parameter_name=statistic_key, parameter_value=statistic_value)
            time.sleep(interval)



    def _create_widgets(self, names_statistic_parametrs:list):
        """
        
        Приватный метод для создания виджетов

        Args:
            statistic_parametrs: массив с именами парметров для создания их виджетов

        """

        # Cоздание заголовка
        window_title = ttk.Label(self._main_frame, text='Загрузка системы', font=("Arial", 16), padding=[0,20])
        window_title.grid(row=0, column=0, columnspan=10, sticky='e')

        # Создание строк статистики
        for index,name_statistic_parametr in enumerate(names_statistic_parametrs):
            self._statistic_parametrs[name_statistic_parametr] = \
                ttk.Label(self._main_frame, text=f'{name_statistic_parametr}: ', font=("Arial", 10))
            
            self._statistic_parametrs[name_statistic_parametr].grid(row=index+1, column=0, columnspan=2, sticky='w')
        
        # Создание фрейма для панели управления функциями
        frame_control_panel = tk.Frame(self._main_frame, pady=20)
        frame_control_panel.grid(row = len(self._statistic_parametrs) + 1, column=0)

        # Создание интерфейса для ввода интервала записи данных
        label_interval_entry = ttk.Label(frame_control_panel, text='Интервал записи(сек): ')
        label_interval_entry.grid(row=0, column=0,sticky='w')

        self._interval_entry = ttk.Entry(frame_control_panel)
        self._interval_entry.grid(row=0, column=1, sticky='w')

        # Создание кнопки для записи данных в бд
        self._button = ttk.Button(frame_control_panel, text='Начать запись', command=self._start_recording)
        self._button.grid(row=1, column=0, sticky='w')


    def _show_error_window(self, erorr_text:str):
        """
        
        Метод для вывода ошибки в отдельном окне

        Args:
            error_text: Текст ошибки

        """

        messagebox.showinfo("Ошибка", erorr_text)
    
    def _set_statistic_value(self, parameter_name:str='None', parameter_value:str = 'None'):
        """
        
        Публичный метод для установки нового значения определенного параметра
        статистики

        Args:
            statistic_name: имя параметра статистики (из ключей self._statistic_parametrs)
            parameter_value: новое значение параметра

        """

        if parameter_name in self._statistic_parametrs:
            self._window.after(0, lambda: self._statistic_parametrs[parameter_name].config(text=f'{parameter_name}: {parameter_value}'))
            # self._statistic_parametrs[parameter_name]['text'] = f'{parameter_name}: {parameter_value}'
        else:
            self._show_error_window(f'Ошибка: Параметр с именем {parameter_name} не найден.')
    
    def run(self):
        """
        
        Запуск главного цикла обработки событий Tkinter

        """

        self._window.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    UI = LoadAnalyzerUI(window)
    UI.run()
