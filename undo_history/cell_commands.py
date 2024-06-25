from undo_history.command import Command


class ToggleEntryCommand(Command):
    def __init__(self, cell_model, number):
        self.cell_model = cell_model
        self.new_value = number
        self.old_value = cell_model.value
        self.old_notes = cell_model.notes[:]

    def execute(self):
        self.cell_model.toggle_entry(self.new_value)

    def undo(self):
        self.cell_model.set_value(self.old_value)
        self.cell_model.set_notes(self.old_notes)

    def redo(self):
        self.execute()


class ToggleNoteCommand(Command):
    def __init__(self, cell_model, number):
        self.cell_model = cell_model
        self.number = number
        self.old_value = cell_model.value
        self.old_notes = cell_model.notes[:]

    def execute(self):
        self.cell_model.toggle_note(self.number)

    def undo(self):
        self.cell_model.set_notes(self.old_notes)

    def redo(self):
        self.execute()
