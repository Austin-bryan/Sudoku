from tkinter import Canvas
from colors import *
from toggle_buttons import NumberButton, Mode, ModeButton


class CellView(Canvas):
    _DEFAULT_COLOR = '#333'         # Color of a cell in its default state
    _HIGHLIGHT_COLOR = '#555'       # Cells in the same house are highlighted when another cell is selected
    _MATCHING_COLOR = '#299'        # Shows all cells with the same number as the selected one
    _CONFLICT_COLOR = '#A33'        # Turns red if there's a conflict in the house
    _PRESS_COLOR = SELECTION_COLOR  # Turn blue when the user selects a cell

    def __init__(self, x, y, parent, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)

        self.x, self.y = x, y
        self.actual_width, self.actual_height = 50, 50

        self.config(width=50, height=50, bg=CellView._DEFAULT_COLOR)
        self._draw_thick_borders()

    def _draw_thick_borders(self):
        """
        Draws thicker borders for every 3rd row and column to delineate the 3x3 subgrids.

        This method checks if the cell is at the border of a 3x3 subgrid and draws a thicker line accordingly.
        """
        thickness_width = 14

        # Only draw lines at the third mark. Corners require both lines
        should_draw_vertical_line = self.y % 3 == 0 and self.y != 0
        should_draw_horizontal_line = self.x % 3 == 0 and self.x != 0

        # Draw left border for each 3rd column
        if should_draw_vertical_line:
            self.create_line(0, 0, 0, 70 if should_draw_horizontal_line else 50, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = 50 + thickness_width  # The border width needs to be considered for the UI to be aligned
            self.config(width=50 + thickness_width / 2)

        # Draw top border for each 3rd row
        if should_draw_horizontal_line:
            self.create_line(0, 0, 70 if should_draw_vertical_line else 50, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = 50 + thickness_width
            self.config(height=50 + thickness_width / 2)
