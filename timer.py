import tkinter as tk
from tkinter import ttk

from utils.constants import BACKGROUND_COLOR


class Timer(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.running = True
        self.time = 0
        self.timer_label = ttk.Label(self)
        self.timer_label.config(font=('Helvetica', 18, 'bold'), background=BACKGROUND_COLOR)
        self.timer_label.pack()
        self.stop()
        self.update_timer()

    def start(self):
        if not self.running:
            self.running = True
            self._update()
            self.timer_label.config(foreground='green')
            self.reset()
        
    def stop(self):
        if self.running:
            self.running = False
            self.timer_label.config(foreground='red')

    def reset(self):
        self.time = 0
        self.update_timer()

    def _update(self):
        if self.running:
            self.time += 1
            self.update_timer()
            self.after(1000, self._update)

    def update_timer(self):
        hours = self.time // 3600
        minutes = (self.time % 3600) // 60
        seconds = self.time % 60
        self.timer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
