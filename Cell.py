import tkinter as tk
from tkinter import Canvas
from Colors import *
from ToggleButtons import NumberButton, Mode, ModeButton


class Cell(Canvas):
    cells: list[list['Cell']] = [[None for _ in range(9)] for _ in range(9)]
    selected_cell = None
    _DEFAULT_COLOR = '#333'
    _HIGHLIGHT_COLOR = '#555'
    _MATCHING_COLOR = '#299'
    _CONFLICT_COLOR = '#A33'
    _PRESS_COLOR = SELECTION_COLOR

    #
    # Initialization Methods
    #
    def __init__(self, parent, x, y, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.x, self.y, self._in_conflict, self._is_highlighted = x, y, False, False
        self.actual_width, self.actual_height = 50, 50

        self.config(width=50, height=50, bg=Cell._DEFAULT_COLOR)
        self.draw_thick_borders()
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind_all("<Up>", self.on_up)
        self.bind_all("<Down>", self.on_down)
        self.bind_all("<Left>", self.on_left)
        self.bind_all("<Right>", self.on_right)
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<Delete>", self.clear_selected)
        self.bind_all("<BackSpace>", self.clear_selected)
        self._active_drafts = []

        # Add a label to the canvas
        self.final_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        # Populate draft numbers
        self.draft_labels = []
        label_index = 1
        for row in range(3):
            for col in range(3):
                x = (col + 1) * self.actual_width / 4
                y = (row + 1) * self.actual_height / 4
                self.draft_labels.append(
                    self.create_text(x, y, fill='white', font=("Arial", 9))
                )
                label_index += 1

        Cell.cells[self.x][self.y] = self

    def draw_thick_borders(self):
        thickness_width = 14
        should_vertical_line = self.y % 3 == 0 and self.y != 0
        should_horizontal_line = self.x % 3 == 0 and self.x != 0

        # Draw left border for each 3rd column
        if should_vertical_line:
            self.create_line(0, 0, 0, 70 if should_horizontal_line else 50, width=thickness_width,
                             fill=BACKGROUND_COLOR)
            self.actual_width = 50 + thickness_width
            self.config(width=50 + thickness_width / 2)

        # Draw top border for each 3rd row
        if should_horizontal_line:
            self.create_line(0, 0, 70 if should_vertical_line else 50, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = 50 + thickness_width
            self.config(height=50 + thickness_width / 2)

    #
    # Event Handlers
    #
    def on_press(self, event):
        # Set selected cell
        Cell.selected_cell = self
        self.focus_set()  # Ensure the cell has focus to receive key events

        # Clear all highlights
        for row in Cell.cells:
            for cell in row:
                if not cell._in_conflict:
                    cell.config(bg=Cell._DEFAULT_COLOR)
                    cell._is_highlighted = False
                else:
                    cell.config(bg=self._CONFLICT_COLOR)
        self.config(bg=self._PRESS_COLOR)

        # Highlight the entire house, ignoring conflicted cells
        for cell in self.get_house():
            if not cell._in_conflict:
                cell.config(bg=Cell._HIGHLIGHT_COLOR)
            cell._is_highlighted = True

        self._highlight_matching_numbers()
        self.show_number_buttons()

    @staticmethod
    def on_up(event):
        Cell.selected_cell.move_selection(-1, 0)

    @staticmethod
    def on_down(event):
        Cell.selected_cell.move_selection(1, 0)

    @staticmethod
    def on_left(event):
        Cell.selected_cell.move_selection(0, -1)

    @staticmethod
    def on_right(event):
        Cell.selected_cell.move_selection(0, 1)

    @staticmethod
    def on_key_press(event):
        if event.keysym not in '123456789':
            return
        if ModeButton.mode == Mode.FINAL:
            Cell.selected_cell.write_final(event.keysym)
        else:
            Cell.selected_cell.toggle_draft(event.keysym)
        Cell.selected_cell.show_number_buttons()

    #
    # Instance Methods
    #
    def _highlight_matching_numbers(self):
        [cell.config(bg=self._MATCHING_COLOR) for cell in self.get_matching_number() if not cell._in_conflict]

    def show_number_buttons(self):
        NumberButton.toggle_all_off()

        if self.is_hint():
            return

        if ModeButton.mode == Mode.FINAL:
            final_text = self._final_number

            if final_text != '':
                NumberButton.toggle_final_on(final_text)
        else:
            NumberButton.toggle_draft_on(self._active_drafts)

    def get_row(self):
        return [Cell.cells[self.x][y] for y in range(9) if Cell.cells[self.x][y] is not self]

    def get_column(self):
        return [Cell.cells[x][self.y] for x in range(9) if Cell.cells[x][self.y] is not self]

    def get_square(self):
        # Determine the starting coordinates of the 3x3 square
        start_x = (self.x // 3) * 3
        start_y = (self.y // 3) * 3

        # Collect all cells in the 3x3 square
        return [
            Cell.cells[i][j]
            for i in range(start_x, start_x + 3)
            for j in range(start_y, start_y + 3)
            if Cell.cells[i][j] is not self
        ]

    def get_house(self):
        return self.get_row() + self.get_column() + self.get_square()

    def find_conflicts(self) -> list['Cell']:
        if not self._has_final_label():
            return []
        conflicting_cells = []
        for cell in self.get_house():
            if cell._final_number == self._final_number:
                conflicting_cells.append(cell)
        return conflicting_cells

    def get_matching_number(self):
        if not self._has_final_label():
            return []
        cells = []

        for layer in Cell.cells:
            for cell in layer:
                if cell is self:
                    continue
                if cell._final_number == self._final_number:
                    cells.append(cell)
        return cells

    @property
    def _final_number(self):
        return self.itemcget(self.final_label, 'text')

    @_final_number.setter
    def _final_number(self, value):
        self.itemconfig(self.final_label, text=value)

    def _has_final_label(self):
        return bool(self._final_number)

    def write_final(self, number):
        self.clear_drafts()

        if self._final_number is not None:
            [cell._update_color(cell._in_conflict) for cell in self.get_matching_number()]
        self._final_number = number

        conflicts = self.find_conflicts()
        self._update_color(conflicts)
        [cell._update_color(True) for cell in conflicts]
        self._update_house_conflict_status(number)

        self.itemconfig(self.final_label, fill='white')
        self._highlight_matching_numbers()

    def _update_house_conflict_status(self, number=None):
        for cell in self.get_house():
            if cell._has_final_label():
                if cell._in_conflict:
                    cell._update_color(cell.find_conflicts())
            elif number is not None:
                cell.clear_draft(number)

    def _update_color(self, in_conflict):
        print(in_conflict, self._is_highlighted)
        self._in_conflict = in_conflict
        self.config(
            bg=self._CONFLICT_COLOR if in_conflict else
            self._HIGHLIGHT_COLOR if self._is_highlighted else
            self._PRESS_COLOR if Cell.selected_cell is self else
            self._DEFAULT_COLOR
        )

    def write_hint(self, number):
        self._final_number = number

    def write_draft(self, number):
        self.clear_final()
        self.itemconfig(self.draft_labels[int(number) - 1], text=str(number))

        if number not in self._active_drafts:
            self._active_drafts.append(number)

    def clear_final(self):
        self._final_number = ''
        self._update_color(False)
        self._update_house_conflict_status()

    def clear_draft(self, number):
        self.itemconfig(self.draft_labels[int(number) - 1], text='')

        if number in self._active_drafts:
            self._active_drafts.remove(number)

    def clear_drafts(self):
        for i in range(9):
            self.clear_draft(i + 1)

    def has_draft(self, number):
        return number in self._active_drafts

    def toggle_draft(self, number):
        if not self._has_final_label():
            for active_draft in self._active_drafts:
                self.write_draft(active_draft)

        if self.has_draft(number):
            self.clear_draft(number)
        else:
            self.write_draft(number)

    def is_hint(self):
        return self._has_final_label() and self.itemcget(self.final_label, 'fill') == 'black'

    def is_incorrect(self):
        return bool(self._final_number)

    def move_selection(self, dx, dy):
        new_x = (self.x + dx) % 9
        new_y = (self.y + dy) % 9
        new_cell = Cell.cells[new_x][new_y]
        if new_cell:
            new_cell.on_press(None)

    #
    # Class Methods
    #
    @classmethod
    def populate_board(cls):
        from SudokuGenerator import SudokuGenerator

        generator = SudokuGenerator()
        numbers = generator.generate_board()

        for x, layer in enumerate(numbers):
            for y, number in enumerate(layer):
                if number != 0:
                    Cell.cells[x][y].write_hint(number)

    @classmethod
    def clear_selected(cls, event):
        if cls.selected_cell._has_final_label():
            Cell.selected_cell._final_number = ''
            cls.selected_cell._update_color(False)
            cls.selected_cell._update_house_conflict_status()
        else:
            cls.selected_cell.clear_drafts()

    @classmethod
    def update_selected_cell(cls, number):
        if Cell.selected_cell is not None and not cls.selected_cell.is_hint():
            if ModeButton.mode == Mode.FINAL:
                cls.selected_cell.write_final(number)
                cls.selected_cell.on_press(None)
            else:
                cls.selected_cell.toggle_draft(number)
