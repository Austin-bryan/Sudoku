from tkinter import *
from abc import ABC
from utils.constants import *

# Colors for different states
BUTTON_DEFAULT_COLOR = '#333'
BUTTON_HOVER_COLOR = '#223'
BUTTON_PRESS_COLOR = SELECTION_COLOR


class GameButton(Canvas):
    def __init__(self, parent, label, width=70, command=None, **kwargs):
        self.WIDTH = width
        self.label = label

        super().__init__(parent, width=self.WIDTH, height=self.WIDTH, highlightthickness=0, **kwargs)

        # Draw the button
        self.rect = self.create_rectangle(0, 0, self.WIDTH, self.WIDTH, fill=BUTTON_DEFAULT_COLOR, outline="")
        self.text = self.create_text(self.WIDTH / 2, self.WIDTH / 2, text=self.label, fill="white", font=("Arial", 18))

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        if command:
            self.bind("<ButtonPress-1>", lambda event: command())
        else:
            self.bind("<ButtonPress-1>", self.on_press)

    def on_enter(self, event):
        """ Applies hover effect. """
        self._set_color(BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        """ Returns to default on mouse leave. """
        self._set_color(BUTTON_DEFAULT_COLOR)

    def on_press(self, event):
        pass

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)
