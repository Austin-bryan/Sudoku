import tkinter as tk
from tkinter import Canvas
from Colors import *
from ToggleButtons import NumberButton, Mode, ModeButton


class Cell(Canvas):
    board: list[list['Cell']] = [[None for _ in range(9)] for _ in range(9)]
    selected_cell = None
    _DEFAULT_COLOR = '#333'         # Color of a cell in its default state
    _HIGHLIGHT_COLOR = '#555'       # Cells in the same house are highlighted when another cell is selected
    _MATCHING_COLOR = '#299'        # Shows all cells with the same number as the selected one
    _CONFLICT_COLOR = '#A33'        # Turns red if there's a conflict in the house
    _PRESS_COLOR = SELECTION_COLOR  # Turn blue when the user selects a cell

    #
    # Initialization Methods
    #
    def __init__(self, parent, x, y, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.x, self.y, self._in_conflict, self._is_highlighted = x, y, False, False

        # When we later add thick borders at the third mark, it requires adjustments to the width and height of the cell
        self.actual_width, self.actual_height = 50, 50

        self.config(width=50, height=50, bg=Cell._DEFAULT_COLOR)
        self._draw_thick_borders()

        # Bind events
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind_all("<Up>", self._on_up)
        self.bind_all("<Down>", self._on_down)
        self.bind_all("<Left>", self._on_left)
        self.bind_all("<Right>", self._on_right)
        self.bind_all("<Key>", self._on_key_press)
        self.bind_all("<Delete>", self.clear_selected)
        self.bind_all("<BackSpace>", self.clear_selected)
        self._active_notes = []

        # Add a label to the canvas
        self.entry_label = self.create_text(self.actual_width / 2, self.actual_height / 2,
                                            text='', fill='black', font=("Arial", 30))
        # Populate notes
        self.note_labels = []
        label_index = 1
        for row in range(3):
            for col in range(3):
                x = (col + 1) * self.actual_width / 4
                y = (row + 1) * self.actual_height / 4
                self.note_labels.append(
                    self.create_text(x, y, fill='white', font=("Arial", 9))
                )
                label_index += 1

        Cell.board[self.x][self.y] = self

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
            self.create_line(0, 0, 0, 70 if should_draw_horizontal_line
                                         else 50, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = 50 + thickness_width  # The border width needs to be considered for the UI to be aligned
            self.config(width=50 + thickness_width / 2)

        # Draw top border for each 3rd row
        if should_draw_horizontal_line:
            self.create_line(0, 0, 70 if should_draw_vertical_line
                                      else 50, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = 50 + thickness_width
            self.config(height=50 + thickness_width / 2)

    #
    # Event Handlers
    #
    def _on_press(self, event):
        Cell.selected_cell = self  # Set selected cell
        self.focus_set()           # Ensure the cell has focus to receive key events

        # Clear all highlights from last selected cell
        for cell in Cell.all_cells():
            # Reset to either default color, or conflict color if in conflict
            if not cell._in_conflict:
                cell.config(bg=Cell._DEFAULT_COLOR)
                cell._is_highlighted = False
            else:
                cell.config(bg=self._CONFLICT_COLOR)
        self.config(bg=self._PRESS_COLOR)

        # Highlight the entire house, ignoring conflicted cells
        for cell in self._get_house():
            if not cell._in_conflict:
                cell.config(bg=Cell._HIGHLIGHT_COLOR)
            # We need to cache the fact that it is highlight,
            # in case the user fixes the conflict to highlight properly
            cell._is_highlighted = True

        self._highlight_matching_numbers()
        self._show_number_buttons()

    @staticmethod
    def _on_up(event):
        Cell.selected_cell._move_selection(-1, 0)

    @staticmethod
    def _on_down(event):
        Cell.selected_cell._move_selection(1, 0)

    @staticmethod
    def _on_left(event):
        Cell.selected_cell._move_selection(0, -1)

    @staticmethod
    def _on_right(event):
        Cell.selected_cell._move_selection(0, 1)

    @staticmethod
    def _on_key_press(event):
        """ Allows the user to enter in numbers, either notes or entries depending on the mode """
        if event.keysym not in '123456789':
            return
        if ModeButton.mode == Mode.ENTRY:
            Cell.selected_cell._write_entry(event.keysym)
        else:
            Cell.selected_cell._toggle_note(event.keysym)
        Cell.selected_cell._show_number_buttons()

    #
    # Instance Methods
    #
    def _highlight_matching_numbers(self):
        """ Highlights all cells with the same number as the selected cell, provided they aren't in conflict """
        [cell.config(bg=self._MATCHING_COLOR) for cell in self._get_matching_numbers() if not cell._in_conflict]

    def _show_number_buttons(self):
        """
        Shows which number button is currently selected.
        In entry mode, this highlights the single entry button, allowing the user to deselect it
        In notes mode, this highlights all selected numbers, so they can deselect whichever they want
        """
        NumberButton.toggle_all_off()

        if self._is_given():
            return
        if ModeButton.mode == Mode.ENTRY:
            if self._has_entry_number():
                NumberButton.toggle_final_on(self._entry_number)
        else:
            NumberButton.toggle_draft_on(self._active_notes)

    def _get_row(self):
        return [Cell.board[self.x][y] for y in range(9) if Cell.board[self.x][y] is not self]

    def _get_column(self):
        return [Cell.board[x][self.y] for x in range(9) if Cell.board[x][self.y] is not self]

    def _get_square(self):
        # Determine the starting coordinates of the 3x3 square
        start_x = (self.x // 3) * 3
        start_y = (self.y // 3) * 3

        # Collect all cells in the 3x3 square
        return [
            Cell.board[i][j]
            for i in range(start_x, start_x + 3)
            for j in range(start_y, start_y + 3)
            if Cell.board[i][j] is not self
        ]

    def _get_house(self):
        """ Returns all cells in the same house, these cells cannot have the same number as self """
        return self._get_row() + self._get_column() + self._get_square()

    def _find_conflicts(self):
        """ Searches the house for conflicts and returns all of them """
        if not self._has_entry_number():
            return []
        conflicting_cells = []

        for cell in self._get_house():
            if cell._entry_number == self._entry_number:
                conflicting_cells.append(cell)
        return conflicting_cells

    def _get_matching_numbers(self):
        """ Returns all cells with the same entry number, even if in a different house """
        if not self._has_entry_number():
            return []
        cells = []

        for cell in Cell.all_cells():
            if cell is self:
                continue
            if cell._entry_number == self._entry_number:
                cells.append(cell)
        return cells

    @property
    def _entry_number(self):
        return self.itemcget(self.entry_label, 'text')

    @_entry_number.setter
    def _entry_number(self, value):
        self.itemconfig(self.entry_label, text=value)

    def _has_entry_number(self):
        return self._entry_number != ''

    def _write_entry(self, number):
        """
        Writes an entry number into a cell, replacing all notes in the cell
        Also toggles off any notes with the same number in the same house
        """

        self._clear_notes()

        if self._entry_number is not None:
            [cell._update_color(cell._in_conflict) for cell in self._get_matching_numbers()]
        self._entry_number = number

        # Check for conflicts and updates house
        conflicts = self._find_conflicts()
        self._update_color(conflicts)
        [cell._update_color(True) for cell in conflicts]
        self._update_house_conflict_status(number)

        self.itemconfig(self.entry_label, fill='white')
        self._highlight_matching_numbers()

    def _update_house_conflict_status(self, number=None):
        """
        Updates the conflict status of all cells in the same house (row, column, or 3x3 grid) as the current cell.

        This method checks each cell in the house to see if it has a number (entry). If it does, and the cell is in
        conflict, it updates the cell's color based on whether there are conflicts. If a number is provided, it clears
        any notes containing that number.

        Parameters:
        number (int, optional): The number to be cleared from notes in the house cells. Defaults to None.
        """
        for cell in self._get_house():
            if cell._has_entry_number():
                if cell._in_conflict:
                    cell._update_color(cell._find_conflicts())
            elif number is not None:
                cell._clear_note(number)

    def _update_color(self, in_conflict):
        self._in_conflict = in_conflict
        self.config(
            bg=self._CONFLICT_COLOR if in_conflict else
            self._HIGHLIGHT_COLOR if self._is_highlighted else
            self._PRESS_COLOR if Cell.selected_cell is self else
            self._DEFAULT_COLOR
        )

    def _write_given(self, number):
        """ This is a number that's provided as a clue. """
        self._entry_number = number

    def _write_note(self, number):
        """
        Clears the entry and writes a note. Also shows any active notes that were cached previously.
        Active notes are cached so if the user decides to remove an entry, all their previous notes are still there
        """
        self._clear_entry()
        self.itemconfig(self.note_labels[int(number) - 1], text=str(number))

        if number not in self._active_notes:
            self._active_notes.append(number)

    def _clear_entry(self):
        self._entry_number = ''
        self._update_color(False)  # An empty cell is always not in conflict
        self._update_house_conflict_status()  # This change may affect house conflict statuses

    def _clear_note(self, number):
        self.itemconfig(self.note_labels[int(number) - 1], text='')

        if number in self._active_notes:
            self._active_notes.remove(number)

    def _clear_notes(self):
        for i in range(9):
            self._clear_note(i + 1)

    def _has_note(self, number):
        return number in self._active_notes

    def _toggle_note(self, number):
        show_active_notes = False

        if self._has_entry_number():
            self._clear_entry()
            show_active_notes = True
        if self._has_note(number):
            self._clear_note(number)
        else:
            self._write_note(number)

        # Active notes are notes that are written but may sometimes be hidden by an entry
        # Since they are preserved even after an entry is made, this restores them for the user
        if show_active_notes:
            for active_note in self._active_notes:
                self._write_note(active_note)

    def _is_given(self):
        return self._has_entry_number() and self.itemcget(self.entry_label, 'fill') == 'black'

    def _move_selection(self, dx, dy):
        """ Move the selection to a new cell based on the delta values """
        new_x = (self.x + dx) % 9
        new_y = (self.y + dy) % 9
        new_cell = Cell.board[new_x][new_y]
        if new_cell:
            new_cell._on_press(None)

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
                    cls.board[x][y]._write_given(number)

    @classmethod
    def clear_selected(cls, event):
        """ Clears any cell, whether that means deleting the entry or removing all notes. Updates conflicts. """
        if cls.selected_cell._has_entry_number():
            Cell.selected_cell._entry_number = ''
            cls.selected_cell._update_color(False)
            cls.selected_cell._update_house_conflict_status()
        else:
            cls.selected_cell._clear_notes()

    @classmethod
    def toggle_selected_cell(cls, number):
        """ Updates the selected cell with the entered number """
        if cls.selected_cell is not None and not cls.selected_cell._is_given():
            if ModeButton.mode == Mode.ENTRY:
                cls.selected_cell._write_entry(number)
                cls.selected_cell._on_press(None)
            else:
                cls.selected_cell._toggle_note(number)

    @classmethod
    def all_cells(cls):
        """ Returns a flat list of all cells in the board """
        return [cell for row in cls.board for cell in row]
