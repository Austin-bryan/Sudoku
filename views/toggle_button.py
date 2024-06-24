from tkinter import *
from abc import ABC
from utils.constants import *
from views.action_button import ActionButton, BUTTON_DEFAULT_COLOR, DEFAULT_FONT_SIZE, DEFAULT_WIDTH

BUTTON_TOGGLE_COLOR = SELECTION_COLOR


class ToggleButton(ActionButton, ABC):
    def __init__(self, parent, label, font_size=DEFAULT_FONT_SIZE, width=DEFAULT_WIDTH, image_path=None, **kwargs):
        super().__init__(parent, label, font_size, width, image_path=image_path, **kwargs)

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
