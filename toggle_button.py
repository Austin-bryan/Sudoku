from tkinter import *
from abc import ABC
from enum import Enum
from colors import *


class ToggleButton(Canvas, ABC):
    # Colors for different states
    _DEFAULT_COLOR = BACKGROUND_COLOR
    _HOVER_COLOR = '#223'
    _TOGGLE_COLOR = SELECTION_COLOR

    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, width=50, height=50, highlightthickness=0, **kwargs)

        self.is_toggled = False  # Toggle state
        self.label = label

        # Draw the button
        self.rect = self.create_rectangle(0, 0, 50, 50, fill=ToggleButton._DEFAULT_COLOR, outline="")
        self.text = self.create_text(25, 25, text=self.label, fill="white", font=("Arial", 18))

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)

    def on_enter(self, event):
        if not self.is_toggled:
            self.itemconfig(self.rect, fill=ToggleButton._HOVER_COLOR)

    def on_leave(self, event):
        if not self.is_toggled:
            self.itemconfig(self.rect, fill=ToggleButton._DEFAULT_COLOR)

    def on_press(self, event):
        if self.is_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self.is_toggled = True
        self.itemconfig(self.rect, fill=ToggleButton._TOGGLE_COLOR)

    def toggle_off(self):
        self.is_toggled = False
        self.itemconfig(self.rect, fill=ToggleButton._DEFAULT_COLOR)