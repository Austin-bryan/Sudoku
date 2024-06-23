from tkinter import *
from abc import ABC
from utils.constants import *
from views.game_button import GameButton, BUTTON_DEFAULT_COLOR

BUTTON_TOGGLE_COLOR = SELECTION_COLOR


class ToggleButton(GameButton, ABC):
    def __init__(self, parent, label, width=70, **kwargs):
        super().__init__(parent, label, width, **kwargs)

        self._is_toggled = False  # Toggle state
        self.label = label

    def on_enter(self, event):
        """ Applies hover effect. """
        if not self._is_toggled:
            super().on_enter(event)

    def on_leave(self, event):
        """ Returns to default on mouse leave. """
        if not self._is_toggled:
            super().on_leave(event)

    def on_press(self, event):
        if self._is_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self._is_toggled = True
        self._set_color(BUTTON_TOGGLE_COLOR)

    def toggle_off(self):
        self._is_toggled = False
        self._set_color(BUTTON_DEFAULT_COLOR)
