import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

        self._main_frame = ttk.Frame(self._window, padding=(20,20)) # Фрейм для отступа 20 пикселей со всех сторон
        self._main_frame.pack(fill="both", expand=True)

        self._statistic_parametrs = {} # Список всех отслеживаемых значений

        self._create_widgets(['CPU', 'RAM', 'ROM'])

    def _create_widgets(self, names_statistic_parametrs:list):
        """
        
        Приватный метод для создания виджетов

        Args:
            statistic_parametrs: массив с именами парметров для создания их виджетов

        """

        # Cоздание заголовка
        window_title = ttk.Label(self._main_frame, text='Загрузка системы', font=("Arial", 16))
        window_title.grid(row=0, column=0, columnspan=2)
        
        # Создание строк статистики
        for index,name_statistic_parametr in enumerate(names_statistic_parametrs):
            self._statistic_parametrs[name_statistic_parametr] = \
                ttk.Label(self._main_frame, text=f'{name_statistic_parametr}: ', font=("Arial", 10))
            
            self._statistic_parametrs[name_statistic_parametr].grid(row=index+1, column=0, columnspan=2, sticky='w')

        btn = ttk.Button(self._main_frame, name='start', command=self.set_statistic_value)
        btn.grid(row=4, column=0, columnspan=2, sticky='w')

    def _show_error_window(self, erorr_text:str):
        """
        
        Метод для вывода ошибки в отдельном окне

        Args:
            error_text: Текст ошибки

        """

        messagebox.showinfo("Ошибка", erorr_text)
    
    def set_statistic_value(self, parameter_name:str='None', parameter_value:str = 'None'):
        """
        
        Публичный метод для установки нового значения определенного параметра
        статистики

        Args:
            statistic_name: имя параметра статистики (из ключей self._statistic_parametrs)
            parameter_value: новое значение параметра

        """

        if parameter_name in self._statistic_parametrs:
            self._statistic_parametrs['CPU'].config(text='wdadw')
            self._statistic_parametrs[parameter_name]['text'] = f'{parameter_name}: {parameter_value}'
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
