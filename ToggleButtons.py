from tkinter import *
from abc import ABC
from enum import Enum
from Colors import *


class ToggleButton(Canvas, ABC):
    # Colors for different states
    __DEFAULT_COLOR = BACKGROUND_COLOR
    __HOVER_COLOR = '#223'
    __TOGGLE_COLOR = SELECTION_COLOR

    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, width=50, height=50, highlightthickness=0, **kwargs)

        self.is_toggled = False  # Toggle state
        self.label = label

        # Draw the button
        self.rect = self.create_rectangle(0, 0, 50, 50, fill=ToggleButton.__DEFAULT_COLOR, outline="")
        self.text = self.create_text(25, 25, text=self.label, fill="white", font=("Arial", 18))

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)

    def on_enter(self, event):
        if not self.is_toggled:
            self.itemconfig(self.rect, fill=ToggleButton.__HOVER_COLOR)

    def on_leave(self, event):
        if not self.is_toggled:
            self.itemconfig(self.rect, fill=ToggleButton.__DEFAULT_COLOR)

    def on_press(self, event):
        if self.is_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self.is_toggled = True
        self.itemconfig(self.rect, fill=ToggleButton.__TOGGLE_COLOR)

    def toggle_off(self):
        self.is_toggled = False
        self.itemconfig(self.rect, fill=ToggleButton.__DEFAULT_COLOR)


class NumberButton(ToggleButton):
    buttons = {}
    __selected_button = None

    @classmethod
    def toggle_all_off(cls):
        [button.toggle_off() for button in cls.buttons.values()]

    @classmethod
    def toggle_final_on(cls, number):
        cls.buttons[number].toggle_on()

    @classmethod
    def toggle_draft_on(cls, draft_numbers):
        for number in draft_numbers:
            cls.buttons[number].toggle_on()

    def __init__(self, parent, number, **kwargs):
        super().__init__(parent, number, **kwargs)
        NumberButton.buttons[number] = self
        self.number = number

    def on_press(self, event):
        if NumberButton.__selected_button is not None and ModeButton.mode == Mode.ENTRY:
            NumberButton.__selected_button.toggle_off()
        NumberButton.__selected_button = self
        super().on_press(self)

        from Cell import Cell
        Cell.toggle_selected_cell(self.number)


class Mode(Enum):
    ENTRY = 0
    NOTES = 1


class ModeButton(ToggleButton):
    mode = Mode.ENTRY

    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, label, **kwargs)

    def on_press(self, event):
        ModeButton.mode = Mode.NOTES if self.mode == Mode.ENTRY else Mode.ENTRY
        from Cell import Cell
        if Cell.selected_cell:
            Cell.selected_cell._show_number_buttons()

        super().on_press(self)
