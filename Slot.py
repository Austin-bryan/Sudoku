import tkinter as tk
from tkinter import *
from Colors import *
from SudokuGenerator import *
from ToggleButtons import NumberButton
from ToggleButtons import Mode
from ToggleButtons import ModeButton


class Slot(Canvas):
    slots = [[None for _ in range(9)] for _ in range(9)]
    selected_slot = None
    __DEFAULT_COLOR = '#333'
    __HIGHLIGHT_COLOR = '#444'
    __Matching_COLOR = '#299'
    __PRESS_COLOR = SELECTION_COLOR

    @classmethod
    def populate_board(cls):
        generator = SudokuGenerator()
        numbers = generator.generate_board()

        for x, layer in enumerate(numbers):
            for y, number in enumerate(layer):
                if number != 0:
                    Slot.slots[x][y].write_hint(number)

    def __init__(self, parent, x, y, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, **kwargs)
        self.x, self.y = x, y

        self.config(width=50, height=50, bg=Slot.__DEFAULT_COLOR)
        self.actual_width, self.actual_height = 50, 50
        self.draw_thick_borders()
        self.bind("<ButtonPress-1>", self.on_press)
        self.__active_drafts = []

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

        # Clear all highlights
        for row in Slot.slots:
            for slot in row:
                slot.config(bg=Slot.__DEFAULT_COLOR)
        self.config(bg=self.__PRESS_COLOR)

        # Highlight this row, column and square
        for slot in self.get_row() + self.get_column() + self.get_square():
            slot.config(bg=Slot.__HIGHLIGHT_COLOR)

        # Highlight matching numbers
        for slot in self.get_matching_number():
            slot.config(bg=Slot.__Matching_COLOR)

        self.show_number_buttons()

    @staticmethod
    def update_selected_slot(number):
        if Slot.selected_slot is not None and not Slot.selected_slot.is_hint():
            if ModeButton.mode == Mode.FINAL:
                Slot.selected_slot.write_final(number)
                Slot.selected_slot.on_press(None)
            else:
                Slot.selected_slot.toggle_draft(number)

    def show_number_buttons(self):
        NumberButton.toggle_all_off()

        if self.is_hint():
            return

        if ModeButton.mode == Mode.FINAL:
            final_text = self.itemcget(self.final_label, 'text')

            if final_text != '':
                NumberButton.toggle_final_on(final_text)
        else:
            NumberButton.toggle_draft_on(self.__active_drafts)

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

    def get_matching_number(self):
        self_text = self.itemcget(self.final_label, 'text')

        if self_text == '':
            return ""
        slots = []

        for layer in Slot.slots:
            for slot in layer:
                if slot is self:
                    continue
                slot_text = slot.itemcget(slot.final_label, 'text')
                if slot_text == self_text:
                    slots.append(slot)
        return slots

    def write_final(self, number):
        self.clear_drafts()
        for slot in self.get_row() + self.get_column() + self.get_square():
            slot.clear_draft(number)
        self.itemconfig(self.final_label, text=str(number))
        self.itemconfig(self.final_label, fill='white')

    def write_hint(self, number):
        self.itemconfig(self.final_label, text=str(number))

    def write_draft(self, number):
        self.clear_final()
        self.itemconfig(self.draft_labels[int(number) - 1], text=str(number))

        if number not in self.__active_drafts:
            self.__active_drafts.append(number)

    def clear_final(self):
        self.itemconfig(self.final_label, text='')

    def clear_draft(self, number):
        self.itemconfig(self.draft_labels[int(number) - 1], text='')

        if number in self.__active_drafts:
            self.__active_drafts.remove(number)

    def clear_drafts(self):
        [self.clear_draft(i + 1) for i in range(9)]

    def has_draft(self, number):
        return number in self.__active_drafts

    def toggle_draft(self, number):
        if self.itemcget(self.final_label, 'text') != '':
            for active_draft in self.__active_drafts:
                self.write_draft(active_draft)

        if self.has_draft(number):
            self.clear_draft(number)
        else:
            self.write_draft(number)

    def is_hint(self):
        return self.itemcget(self.final_label, 'text') != '' and self.itemcget(self.final_label, 'fill') == 'black'