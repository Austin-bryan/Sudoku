from models.cell_value_type import CellValueType


class CellModel:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.value, self.notes = '', []
        self.in_conflict = False
        self.value_type = CellValueType.BLANK

    def set_entry(self, number):
        if self.value_type == CellValueType.HINT:
            return
        self.value = number
        self.value_type = CellValueType.ENTRY

    def set_hint(self, number):
        self.value = number
        self.value_type = CellValueType.HINT

    def clear_entry(self):
        self.value = ''
        self.in_conflict = False
        self.value_type = CellValueType.BLANK

    def toggle_note(self, number):
        if self.value_type == CellValueType.HINT:
            return
        if number in self.notes:
            self.notes.remove(number)
        else:
            self.notes.append(number)

    def remove_note(self, number):
        if number in self.notes:
            self.notes.remove(number)

    def set_conflict(self, state):
        self.in_conflict = state

    def clear_notes(self):
        self.notes.clear()

    def is_entry(self):
        return self.value_type == CellValueType.ENTRY

    def is_hint(self):
        return self.value_type == CellValueType.HINT

    def has_value(self):
        return self.value != ''
