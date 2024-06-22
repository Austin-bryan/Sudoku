from tkinter import Canvas
from utils.constants import SELECTION_COLOR, BACKGROUND_COLOR, SUBGRID_SIZE
from models.cell_value_type import CellValueType


class CellView(Canvas):
    _DEFAULT_COLOR = '#333'
    _HIGHLIGHT_COLOR = '#4a4a4a'
    _MATCHING_COLOR = '#299'
    _CONFLICT_COLOR = '#A33'
    _PRESS_COLOR = SELECTION_COLOR
    _WIDTH = 70

    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.model = model
        self.actual_width = CellView._WIDTH
        self.actual_height = CellView._WIDTH
        self.config(width=CellView._WIDTH, height=CellView._WIDTH, bg=CellView._DEFAULT_COLOR)
        self._draw_thick_borders()
        self.on_press_event = None
        self._is_highlighted = False

        self.value_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        self.note_labels = [self.create_text((col + 1) * self.actual_width / 4,
                                             (row + 1) * self.actual_height / 4, fill='white', font=("Arial", 9))
                            for row in range(SUBGRID_SIZE) for col in range(SUBGRID_SIZE)]

    def _draw_thick_borders(self):
        """
        Draws the thicker lines on cells that are on the edge of a subgrid.

        Because this changes the length of the cell, the cell has to be made even long to accommodate them.
        """
        thickness_width = 8
        should_draw_vertical_line = self.model.y % SUBGRID_SIZE == 0 and self.model.y != 0
        should_draw_horizontal_line = self.model.x % SUBGRID_SIZE == 0 and self.model.x != 0
        line_length = CellView._WIDTH * 1.4

        if should_draw_vertical_line:
            self.create_line(0, 0, 0, line_length if should_draw_horizontal_line
                                                  else CellView._WIDTH, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = CellView._WIDTH + thickness_width
            self.config(width=CellView._WIDTH + thickness_width / 2)

        if should_draw_horizontal_line:
            self.create_line(0, 0, line_length if should_draw_vertical_line
                                               else CellView._WIDTH, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = CellView._WIDTH + thickness_width
            self.config(height=CellView._WIDTH + thickness_width / 2)

    def update_color(self, color):
        self.config(bg=color)

    def update_labels(self):
        """
        Ensures that labels are set properly depending on the value type of the cell.
        Makes sures notes and entries cannot be visible at the same time, and the color of the value is also correct.
        """
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
        """ Removes the entry label. """
        self.itemconfig(self.value_label, text='')

    def clear_notes(self):
        """ Removes all notes. """
        for label in self.note_labels:
            self.itemconfig(label, text='')

    def set_conflict_status(self, status):
        self.model.in_conflict = status
        self.update_color(CellView._CONFLICT_COLOR if status
                          else CellView._HIGHLIGHT_COLOR if self._is_highlighted
                          else CellView._DEFAULT_COLOR)
