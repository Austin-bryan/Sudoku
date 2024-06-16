import tkinter as tk
from tkinter import Canvas
from Colors import *
from SudokuGenerator import SudokuGenerator
from ToggleButtons import NumberButton, Mode, ModeButton


class Slot(Canvas):
    slots: list[list['Slot']] = [[None for _ in range(9)] for _ in range(9)]
    selected_slot = None
    _DEFAULT_COLOR = '#333'
    _HIGHLIGHT_COLOR = '#444'
    _MATCHING_COLOR = '#299'
    _CONFLICT_COLOR = '#A33'
    _PRESS_COLOR = SELECTION_COLOR

    @classmethod
    def populate_board(cls):
        generator = SudokuGenerator()
        numbers = generator.generate_board()

        for x, layer in enumerate(numbers):
            for y, number in enumerate(layer):
                if number != 0:
                    Slot.slots[x][y].write_hint(number)

    @staticmethod
    def update_selected_slot(number):
        if Slot.selected_slot is not None and not Slot.selected_slot.is_hint():
            if ModeButton.mode == Mode.FINAL:
                Slot.selected_slot.write_final(number)
                Slot.selected_slot.on_press(None)
            else:
                Slot.selected_slot.toggle_draft(number)

    def __init__(self, parent, x, y, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.x, self.y, self._in_conflict = x, y, False
        self.actual_width, self.actual_height = 50, 50

        self.config(width=50, height=50, bg=Slot._DEFAULT_COLOR)
        self.draw_thick_borders()
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind_all("<Up>", self.on_up)
        self.bind_all("<Down>", self.on_down)
        self.bind_all("<Left>", self.on_left)
        self.bind_all("<Right>", self.on_right)
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<Delete>", self.clear)
        self.bind_all("<BackSpace>", self.clear)
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

        Slot.slots[self.x][self.y] = self

    def draw_thick_borders(self):
        thickness_width = 14
        should_vertical_line = self.y % 3 == 0 and self.y != 0
        should_horizontal_line = self.x % 3 == 0 and self.x != 0

        # Draw left border for each 3rd column
        if should_vertical_line:
            self.create_line(0, 0, 0, 70 if should_horizontal_line else 50, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_width = 50 + thickness_width
            self.config(width=50 + thickness_width / 2)

        # Draw top border for each 3rd row
        if should_horizontal_line:
            self.create_line(0, 0, 70 if should_vertical_line else 50, 0, width=thickness_width, fill=BACKGROUND_COLOR)
            self.actual_height = 50 + thickness_width
            self.config(height=50 + thickness_width / 2)

    def on_press(self, event):
        # Set selected slot
        Slot.selected_slot = self
        self.focus_set()  # Ensure the slot has focus to receive key events

        # Clear all highlights
        for row in Slot.slots:
            for slot in row:
                if not slot._in_conflict:
                    slot.config(bg=Slot._DEFAULT_COLOR)
                else:
                    slot.config(bg=self._CONFLICT_COLOR)
        self.config(bg=self._PRESS_COLOR)

        # Highlight this row, column and square
        for slot in self.get_row() + self.get_column() + self.get_square():
            if not slot._in_conflict:
                slot.config(bg=Slot._HIGHLIGHT_COLOR)

        # Highlight matching numbers
        for slot in self.get_matching_number():
            if not slot._in_conflict:
                slot.config(bg=Slot._MATCHING_COLOR)

        self.show_number_buttons()

    def show_number_buttons(self):
        NumberButton.toggle_all_off()

        if self.is_hint():
            return

        if ModeButton.mode == Mode.FINAL:
            final_text = self.itemcget(self.final_label, 'text')

            if final_text != '':
                NumberButton.toggle_final_on(final_text)
        else:
            NumberButton.toggle_draft_on(self._active_drafts)

    def get_row(self):
        return [Slot.slots[self.x][y] for y in range(9) if Slot.slots[self.x][y] is not self]

    def get_column(self):
        return [Slot.slots[x][self.y] for x in range(9) if Slot.slots[x][self.y] is not self]

    def get_square(self):
        # Determine the starting coordinates of the 3x3 square
        start_x = (self.x // 3) * 3
        start_y = (self.y // 3) * 3

        # Collect all slots in the 3x3 square
        return [
            Slot.slots[i][j]
            for i in range(start_x, start_x + 3)
            for j in range(start_y, start_y + 3)
            if Slot.slots[i][j] is not self
        ]

    def get_house(self):
        return self.get_row() + self.get_column() + self.get_square()

    def find_conflicts(self) -> list['Slot']:
        if not self._has_final_label():
            return []
        conflicting_slots = []
        for slot in self.get_house():
            if slot._final_number == self._final_number:
                conflicting_slots.append(slot)
        return conflicting_slots

    def get_matching_number(self):
        if not self._has_final_label():
            return []
        slots = []

        for layer in Slot.slots:
            for slot in layer:
                if slot is self:
                    continue
                if slot._final_number == self._final_number:
                    slots.append(slot)
        return slots

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
        self._final_number = number

        conflicts = self.find_conflicts()
        self._show_conflict(conflicts)
        if conflicts:
            for slot in conflicts:
                slot._show_conflict(True)

        for slot in self.get_house():
            if slot._has_final_label():
                if slot._in_conflict:
                    slot._show_conflict(slot.find_conflicts())
            else:
                slot.clear_draft(number)
        self.itemconfig(self.final_label, fill='white')

    def _show_conflict(self, is_error):
        self._in_conflict = is_error
        self.config(bg=self._CONFLICT_COLOR if is_error else self._DEFAULT_COLOR)

    def write_hint(self, number):
        self._final_number = number

    def write_draft(self, number):
        self.clear_final()
        self.itemconfig(self.draft_labels[int(number) - 1], text=str(number))

        if number not in self._active_drafts:
            self._active_drafts.append(number)

    def clear_final(self):
        self._final_number = ''

    def clear_draft(self, number):
        self.itemconfig(self.draft_labels[int(number) - 1], text='')

        if number in self._active_drafts:
            self._active_drafts.remove(number)

    def clear_drafts(self):
        [self.clear_draft(i + 1) for i in range(9)]

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
        if self.itemcget(self.final_label, 'text') == '':
            return False
        return True

    @staticmethod
    def on_up(event):
        Slot.selected_slot.move_selection(-1, 0)

    @staticmethod
    def on_down(event):
        Slot.selected_slot.move_selection(1, 0)

    @staticmethod
    def on_left(event):
        Slot.selected_slot.move_selection(0, -1)

    @staticmethod
    def on_right(event):
        Slot.selected_slot.move_selection(0, 1)

    def move_selection(self, dx, dy):
        new_x = (self.x + dx) % 9
        new_y = (self.y + dy) % 9
        new_slot = Slot.slots[new_x][new_y]
        if new_slot:
            new_slot.on_press(None)

    @staticmethod
    def on_key_press(event):
        if event.keysym not in '123456789':
            return
        if ModeButton.mode == Mode.FINAL:
            Slot.selected_slot.write_final(event.keysym)
        else:
            Slot.selected_slot.toggle_draft(event.keysym)
        Slot.selected_slot.show_number_buttons()

    @staticmethod
    def clear(event):
        if Slot.selected_slot._has_final_label():
            Slot.selected_slot._final_number = ''
        else:
            Slot.selected_slot.clear_drafts()
