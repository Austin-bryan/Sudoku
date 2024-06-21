from tkinter import Canvas
from utils.constants import SELECTION_COLOR, BACKGROUND_COLOR, SUBGRID_SIZE
from models.cell_value_type import CellValueType


class CellView(Canvas):
    _DEFAULT_COLOR = '#333'
    _HIGHLIGHT_COLOR = '#4a4a4a'
    _MATCHING_COLOR = '#299'
    _CONFLICT_COLOR = '#A33'
    _PRESS_COLOR = SELECTION_COLOR
    _CELL_WIDTH = 70

    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.model = model
        self.actual_width = CellView._CELL_WIDTH
        self.actual_height = CellView._CELL_WIDTH
        self.config(width=CellView._CELL_WIDTH, height=CellView._CELL_WIDTH, bg=CellView._DEFAULT_COLOR)
        self._draw_thick_borders()
        self.on_press_event = None

        self.value_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        self.note_labels = [self.create_text((col + 1) * self.actual_width / 4,
                                             (row + 1) * self.actual_height / 4, fill='white', font=("Arial", 9))
                            for row in range(SUBGRID_SIZE) for col in range(SUBGRID_SIZE)]

    def _draw_thick_borders(self):
        thickness_width = 8
        should_draw_vertical_line = self.model.y % SUBGRID_SIZE == 0 and self.model.y != 0
        should_draw_horizontal_line = self.model.x % SUBGRID_SIZE == 0 and self.model.x != 0
        line_length = CellView._CELL_WIDTH * 1.4

        if should_draw_vertical_line:
            self.create_line(0, 0, 0, line_length if should_draw_horizontal_line
                                                  else CellView._CELL_WIDTH, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = CellView._CELL_WIDTH + thickness_width
            self.config(width=CellView._CELL_WIDTH + thickness_width / 2)

        if should_draw_horizontal_line:
            self.create_line(0, 0, line_length if should_draw_vertical_line
                                               else CellView._CELL_WIDTH, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = CellView._CELL_WIDTH + thickness_width
            self.config(height=CellView._CELL_WIDTH + thickness_width / 2)

    def update_color(self, color):
        self.config(bg=color)

    def update_labels(self):
        match self.model.value_type:
            case CellValueType.ENTRY:
                self.itemconfig(self.value_label,
                                text=self.model.value if self.model.value is not None else '',
                                fill='white')
                self.clear_notes()
            case CellValueType.NOTES:
                self.clear_entry()

                for i, label in enumerate(self.note_labels):
                    self.itemconfig(label, text=i + 1 if self.model.notes[i] else '')
            case CellValueType.GIVEN:
                self.itemconfig(self.value_label, text=self.model.value, fill='black')
            case _:
                self.clear_entry()
                self.clear_notes()

    def clear_entry(self):
        self.itemconfig(self.value_label, text='')

    def clear_notes(self):
        for label in self.note_labels:
            self.itemconfig(label, text='')
