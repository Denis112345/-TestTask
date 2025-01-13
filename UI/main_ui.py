import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from data_processing.main_data_processing import SystemMonitor
from database_requesting.database_handlers import add_statistic

class LoadAnalyzerUI:
    def __init__(self, window:tk.Tk):
        """

        Инициализация класса

        Args:
            window: Главное окно Tkinter

        """

        # Инициализация окна программы
        self._window = window
        self._window.title('Load Analyzer')
        self._window.geometry('400x300')

        # Флаг для отдельного потока с обновлением данных статистики
        self._auto_update_flag = True

        # Параметры для секундомера
        self._start_time = None
        self._elapsed_time = 0
        self._time_counter_flag = False

        # Создание отдельного фрейма для отступов
        self._main_frame = ttk.Frame(self._window, padding=(20,20))
        self._main_frame.pack(fill="both", expand=True)

        # Список всех отслеживаемых значений
        self._statistic_parametrs = {} 

        # Инициализация всех виджетов
        self._create_widgets(['CPU', 'RAM', 'ROM'])

        # Создание отдельного потока для обновления данных статистикаи в UI
        self.update_thread = threading.Thread(target=self._start_statistic_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def _start_statistic_loop(self):
        """
        Функция для постоянного обновления данных статистики
        """
        while self._auto_update_flag:
            try:
                interval = self._interval_entry.get()
                interval = int(interval)
                if interval < 1:
                    interval = 1
                if interval >= 100:
                    interval = 10
            except:
                interval = 1
            self._set_all_statistics(interval)
            time.sleep(interval)
    
    def _stop_statistic_loop(self):
        """
        Функция остановки обновления статистики
        """
        self._auto_update_flag = False

    def _set_all_statistics(self, interval):
        """
        Функция устанавливающая новые данные статисики
        Args:
            interval: Интервал обновления статистики
        """
        system_statistics = SystemMonitor.get_system_resorces(interval=interval)

        for statistic_key, statistic_value in system_statistics.items():
            self._set_statistic_value(parameter_name=statistic_key, parameter_value=statistic_value)

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

    def _show_error_window(self, erorr_text:str):
        """
        
        Метод для вывода ошибки в отдельном окне

        Args:
            error_text: Текст ошибки

        """

        messagebox.showinfo("Ошибка", erorr_text)

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
            self._statistic_parametrs[name_statistic_parametr] = ttk.Label(self._main_frame, text=f'{name_statistic_parametr}: ', font=("Arial", 10))
            
            self._statistic_parametrs[name_statistic_parametr].grid(row=index+1, column=0, columnspan=2, sticky='w')
        
        # Создание фрейма для панели управления функциями
        frame_control_panel = tk.Frame(self._main_frame, pady=20)
        frame_control_panel.grid(row = len(self._statistic_parametrs) + 1, column=0)

        # Создание интерфейса для ввода интервала записи данных
        label_interval_entry = ttk.Label(frame_control_panel, text='Интервал обновления(сек): ')
        label_interval_entry.grid(row=0, column=0,sticky='w')

        self._interval_entry = ttk.Entry(frame_control_panel)
        self._interval_entry.grid(row=0, column=1, sticky='w')

        # Создание кнопки для записи данных в бд
        self._button = ttk.Button(frame_control_panel, text='Начать запись', command=self._start_recording_statistics)
        self._button.grid(row=1, column=0, sticky='w')

        # Создание кнопки для записи данных в бд
        self._time_count_label = ttk.Label(frame_control_panel, text='00:00')
        self._time_count_label.grid(row=2, column=0, sticky='w')

    def _change_time_button(self):
        """
        Функция для замены надписи на кнопки старта записи
        """
        if self._button['text'] != 'Остановить':
            self._button['text'] = 'Остановить'
            return
        
        self._button['text'] = 'Начать запись'

    def requesting_statistic_data_loop(self):
        """
        Функция для добавления статистики в БД, в течении секундомера
        """
        if self._time_counter_flag:
            statistic_data = {}
            for _,statistic_parametr_value in self._statistic_parametrs.items():
                key,value = statistic_parametr_value['text'].split(': ')
                statistic_data[key] = value

            add_statistic(statistic_data)

            try:
                interval = self._interval_entry.get()
                interval = int(interval)
                if interval < 1:
                    interval = 1
            except:
                interval = 1
            
            self._window.after(interval*1000, self.requesting_statistic_data_loop)

    def _start_recording_statistics(self):
        """
        Изменяет назвние кнопки, запускает таймер и создает поток с обновленем
        статистики
        """
        self._change_time_button()
        self._button['command'] = self._stop_recording_statistics
        self._start_time_counter()
        self.requesting_statistic_data_loop()

    def _stop_recording_statistics(self):
        """
        Останавливает запись данных статистики в БД
        """
        self._change_time_button()
        self._button['command'] = self._start_recording_statistics
        self._stop_time_counter()

    def _start_time_counter(self):
        """
        Функция для старта секундомера
        """
        if not self._time_counter_flag:
            self._start_time = time.time()
            self._time_counter_flag = True

            self._update_time_counter()
    
    def _stop_time_counter(self):
        """
        Функция для стопа секундомера
        """
        if self._time_counter_flag:
            self._time_counter_flag = False
            self._reset_time_counter()
            self._change_time_button()
    
    def _reset_time_counter(self):
        """
        Функция для очистики секундомера
        """
        self._time_counter_flag = False
        self._elapsed_time = 0
        self._update_time_counter_ui()

    def _update_time_counter(self):
        """
        Функция для обновления значний для секундомера
        """
        if self._time_counter_flag:
            self._elapsed_time = time.time() - self._start_time
            self._update_time_counter_ui()
            self._window.after(1000, self._update_time_counter)
    
    def _update_time_counter_ui(self):
        """
        Функция обновления UI секундомера
        """
        minutes, seconds = divmod(self._elapsed_time, 60)
        time_str = f'{int(minutes):02}:{int(seconds):02}'
        self._time_count_label['text'] = time_str
    

    def run(self):
        """
        
        Запуск главного цикла обработки событий Tkinter

        """

        self._window.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    UI = LoadAnalyzerUI(window)
    UI.run()