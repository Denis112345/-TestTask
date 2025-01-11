import tkinter as tk
from UI.main_ui import LoadAnalyzerUI


def main():
    window = tk.Tk()
    UI = LoadAnalyzerUI(window)
    UI.run()

if __name__ == '__main__':
    main()