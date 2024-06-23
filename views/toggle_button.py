from tkinter import *
from abc import ABC
from utils.constants import *


class ToggleButton(Canvas, ABC):
    # Colors for different states
    _DEFAULT_COLOR = '#333'
    _HOVER_COLOR = '#223'
    _TOGGLE_COLOR = SELECTION_COLOR

    def __init__(self, parent, label, width=70, **kwargs):
        self.WIDTH = width

        super().__init__(parent, width=self.WIDTH, height=self.WIDTH, highlightthickness=0, **kwargs)

        self._is_toggled = False  # Toggle state
        self.label = label

        # Draw the button
        self.rect = self.create_rectangle(0, 0, self.WIDTH, self.WIDTH, fill=ToggleButton._DEFAULT_COLOR, outline="")
        self.text = self.create_text(self.WIDTH / 2, self.WIDTH / 2, text=self.label, fill="white", font=("Arial", 18))

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)

    def on_enter(self, event):
        """ Applies hover effect. """
        if not self._is_toggled:
            self._set_color(ToggleButton._HOVER_COLOR)

    def on_leave(self, event):
        """ Returns to default on mouse leave. """
        if not self._is_toggled:
            self._set_color(ToggleButton._DEFAULT_COLOR)

    def on_press(self, event):
        if self._is_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self._is_toggled = True
        self._set_color(ToggleButton._TOGGLE_COLOR)

    def toggle_off(self):
        self._is_toggled = False
        self._set_color(ToggleButton._DEFAULT_COLOR)

    def _set_color(self, color):
        self.itemconfig(self.rect, fill=color)
