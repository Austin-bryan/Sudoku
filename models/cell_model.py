class CellModel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.entry_number = ''
        self.notes = []
        self.in_conflict = False

    def add_entry(self, number):
        self.entry_number = number
        self.notes.clear()

    def remove_entry(self):
        self.entry_number = ''
        self.in_conflict = False

    def add_note(self, number):
        if number not in self.notes:
            self.notes.append(number)

    def remove_note(self, number):
        if number in self.notes:
            self.notes.remove(number)

    def has_entry(self):
        return self.entry_number != ''

    def set_conflict(self, state):
        self.in_conflict = state

    def clear_notes(self):
        self.notes.clear()
