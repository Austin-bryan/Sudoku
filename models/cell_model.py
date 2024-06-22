﻿from models.cell_value_type import CellValueType
from models.subject import Subject
from utils.constants import BOARD_SIZE


class CellModel(Subject):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.value, self.notes = None, [False] * BOARD_SIZE
        self.in_conflict = False
        self.value_type = CellValueType.BLANK
        self.house_manager = None

    def toggle_entry(self, number):
        """
        Toggles an entry on or off.
        Notes are not cleared during this process, so that they can be restored again later.
        """
        if self.is_given():
            return
        if self.value == number:
            self.value = None
            self.value_type = CellValueType.NOTES if any(self.notes) else CellValueType.BLANK
        else:
            self.value = number
            self.value_type = CellValueType.ENTRY
        self.notify()

    def set_given(self, number):
        """ Once a cell is set to given, it can never be changed to another cell value type. """
        self.value = number
        self.value_type = CellValueType.GIVEN
        self.notify()

    def clear_cell(self):
        """ Clears all contents of the cell, both value and all notes. Sets the state back to BLANK. """
        if self.is_given():
            return
        self.value = None
        self.in_conflict = False
        self.notes = [False] * BOARD_SIZE
        self.value_type = CellValueType.BLANK
        self.notify()

    def toggle_note(self, number):
        """ Turns a note on or off. """
        if self.is_given():
            return
        self.value = None
        self.notes[number - 1] = not self.notes[number - 1]
        self.value_type = CellValueType.NOTES if any(self.notes) else CellValueType.BLANK
        self.notify()

    def set_conflict_status(self, state):
        self.in_conflict = state
        self.notify()

    def is_entry(self):
        return self.value_type == CellValueType.ENTRY

    def is_given(self):
        return self.value_type == CellValueType.GIVEN

    def is_notes(self):
        return self.value_type == CellValueType.NOTES

    def is_blank(self):
        return self.value_type == CellValueType.BLANK

    def has_value(self):
        return self.value is not None

    def has_note(self, number):
        """ Returns true if the cell has the note of the specified number active. """
        return self.notes[number - 1]

    def get_house(self):
        return self.house_manager.get_house()

    def get_row(self):
        return self.house_manager.get_row()

    def get_column(self):
        return self.house_manager.get_column()

    def get_subgrid(self):
        return self.house_manager.get_subgrid()
