# view/cell_view.py
import tkinter as tk
from tkinter import Canvas
from colors import SELECTION_COLOR, BACKGROUND_COLOR
from models.cell_value_type import CellValueType


class CellView(Canvas):
    _DEFAULT_COLOR = '#333'
    _HIGHLIGHT_COLOR = '#555'
    _MATCHING_COLOR = '#299'
    _CONFLICT_COLOR = '#A33'
    _PRESS_COLOR = SELECTION_COLOR

    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.model = model
        self.actual_width = 50
        self.actual_height = 50
        self.config(width=50, height=50, bg=CellView._DEFAULT_COLOR)
        self._draw_thick_borders()
        self.on_press_event = None

        self.entry_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        self.note_labels = [self.create_text((col + 1) * self.actual_width / 4,
                                             (row + 1) * self.actual_height / 4, fill='white', font=("Arial", 9))
                            for row in range(3) for col in range(3)]

    def _draw_thick_borders(self):
        thickness_width = 8
        should_draw_vertical_line = self.model.y % 3 == 0 and self.model.y != 0
        should_draw_horizontal_line = self.model.x % 3 == 0 and self.model.x != 0

        if should_draw_vertical_line:
            self.create_line(0, 0, 0, 70 if should_draw_horizontal_line else 50, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = 50 + thickness_width
            self.config(width=50 + thickness_width / 2)

        if should_draw_horizontal_line:
            self.create_line(0, 0, 70 if should_draw_vertical_line else 50, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = 50 + thickness_width
            self.config(height=50 + thickness_width / 2)

    def update_color(self, color):
        self.config(bg=color)

    def update_labels(self):
        match self.model.value_type:
            case CellValueType.ENTRY:
                self.itemconfig(self.entry_label,
                                text=self.model.value if self.model.value is not None else '',
                                fill='white')
                self.clear_notes()
            case CellValueType.NOTES:
                self.clear_entry()

                for i, label in enumerate(self.note_labels):
                    self.itemconfig(label, text=i + 1 if self.model.notes[i] else '')
            case CellValueType.GIVEN:
                self.itemconfig(self.entry_label, text=self.model.value, fill='black')
            case _:
                self.clear_entry()
                self.clear_notes()

    def clear_entry(self):
        self.itemconfig(self.entry_label, text='')

    def clear_notes(self):
        for label in self.note_labels:
            self.itemconfig(label, text='')
