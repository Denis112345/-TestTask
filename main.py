import asyncio
import tkinter as tk
from UI.main_ui import LoadAnalyzerUI



async def run_ui():
    window = tk.Tk()
    UI = LoadAnalyzerUI(window)
    UI.run()

async def main():
    run_ui_task = asyncio.create_task(run_ui())

window = tk.Tk()
UI = LoadAnalyzerUI(window)
UI.run()

