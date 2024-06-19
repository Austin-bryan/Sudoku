from tkinter import *
from abc import ABC
from enum import Enum
from colors import *


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
    def toggle_entry_on(cls, number):
        if number:
            # print(type(number), number)
            cls.buttons[number].toggle_on()

    @classmethod
    def toggle_note_on(cls, notes):
        for i, should_toggle_on in enumerate(notes):
            if should_toggle_on:
                cls.buttons[i + 1].toggle_on()

    def __init__(self, parent, board_controller, number, **kwargs):
        super().__init__(parent, number, **kwargs)
        NumberButton.buttons[int(number)] = self
        self.board_controller = board_controller
        self.number = number

    def on_press(self, event):
        if NumberButton.__selected_button is not None and ModeButton.mode == Mode.ENTRY:
            NumberButton.__selected_button.toggle_off()
        NumberButton.__selected_button = self
        super().on_press(self)

        self.board_controller.toggle_selected_cell(self.number)

    @classmethod
    def show_number_buttons(cls, cell_controller):
        cls.toggle_all_off()
        if ModeButton.mode == Mode.ENTRY:
            cls.toggle_entry_on(cell_controller.model.value)
        elif ModeButton.mode == Mode.NOTES:
            cls.toggle_note_on(cell_controller.model.notes)


class Mode(Enum):
    ENTRY = 0
    NOTES = 1


class ModeButton(ToggleButton):
    mode = Mode.ENTRY

    def __init__(self, parent, board_controller, label, **kwargs):
        super().__init__(parent, label, **kwargs)
        self.board_controller = board_controller

    def on_press(self, event):
        ModeButton.mode = Mode.NOTES if self.mode == Mode.ENTRY else Mode.ENTRY

        from controllers.cell_controller import CellController
        if self.board_controller.selected_cell:
            NumberButton.show_number_buttons(self.board_controller.selected_cell)

        super().on_press(self)
