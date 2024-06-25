from undo_history.command import Command


class ToggleEntryCommand(Command):
    count = 0

    def __init__(self, cell_controller, number):
        self.cell_controller = cell_controller
        self.cell_model = cell_controller.model
        self.board_model = cell_controller.board_controller.model
        self.new_value = number
        self.old_value = self.cell_model.value
        self.old_notes = self.cell_model.notes[:]

        ToggleEntryCommand.count += 1
        self.id = ToggleEntryCommand.count

    def execute(self):
        self.cell_model.toggle_entry(self.new_value)

    def undo(self):
        self.cell_model.value = self.old_value
        self.cell_model.notes = self.old_notes[:]
        # self.cell_view.update()
        self.board_model.notify()
        self.cell_model.notify()

    def redo(self):
        self.execute()
        self.board_model.notify()
        # self.cell_model.notify()


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
