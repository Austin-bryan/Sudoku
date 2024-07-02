import tkinter as tk
from tkinter import ttk

from utils.constants import BACKGROUND_COLOR


class Timer(tk.Canvas):
    """ Timer for the game. Starts on first cell selected and ends when game is solved. """
    def __init__(self, parent: tk.Frame, **kwargs):
        super().__init__(parent, **kwargs)
        self.running = True
        self.time = 0
        self.timer_label = ttk.Label(self)
        self.timer_label.config(font=('Helvetica', 18, 'bold'), background=BACKGROUND_COLOR)
        self.timer_label.pack()
        self.stop()
        self.update_timer()

    def start(self):
        """ Start the timer if not already started. Changes the color to green. """
        if self.running:
            return
        self.running = True
        self._update()
        self.timer_label.config(foreground='green')
        self.reset()

    def stop(self):
        """ Stops the timer and reset to red. """
        if not self.running:
            return
        self.running = False
        self.timer_label.config(foreground='red')

    def reset(self):
        """ Resets the timer to the initial state. """
        self.time = 0
        self.update_timer()

    def _update(self):
        """ Continues to tick once per second. """
        if not self.running:
            return
        self.time += 1
        self.update_timer()
        self.after(1000, self._update)

    def update_timer(self):
        """ Updates the display of the timer to represent how much time has passed. """
        hours = self.time // 3600
        minutes = (self.time % 3600) // 60
        seconds = self.time % 60
        self.timer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
