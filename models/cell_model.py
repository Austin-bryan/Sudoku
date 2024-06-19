﻿from models.cell_value_type import CellValueType


class CellModel:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.value, self.notes = None, [False for _ in range(9)]
        self.in_conflict = False
        self.value_type = CellValueType.BLANK

    def toggle_entry(self, number):
        if self.is_given():
            return
        if self.value == number:
            self.value = None
            self.value_type = CellValueType.NOTES if any(self.notes) else CellValueType.BLANK
        else:
            self.value = number
            self.value_type = CellValueType.ENTRY

    def set_given(self, number):
        self.value = number
        self.value_type = CellValueType.GIVEN

    def clear(self):
        if self.is_given():
            return
        self.value = None
        self.in_conflict = False
        self.notes = [False for _ in range(9)]
        self.value_type = CellValueType.BLANK

    def toggle_note(self, number):
        if self.is_given():
            return
        self.value = None
        self.notes[number - 1] = not self.notes[number - 1]
        self.value_type = CellValueType.NOTES if any(self.notes) else CellValueType.BLANK

    def set_conflict(self, state):
        self.in_conflict = state

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
        return self.notes[number - 1]
