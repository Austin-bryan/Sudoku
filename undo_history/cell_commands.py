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
        self.old_value_type = self.cell_model.value_type
        self.old_house_states = self._get_house_states()

        ToggleEntryCommand.count += 1
        self.id = ToggleEntryCommand.count

    def _get_house_states(self):
        """ Get the state of all cells in the same house (row, column, subgrid). """
        house_states = []
        house_cells = self.cell_controller.get_house()  # Assuming get_house() returns all related cells

        for cell in house_cells:
            house_states.append({
                'cell': cell,
                'value': cell.model.value,
                'notes': cell.model.notes[:],
                'value_type': cell.model.value_type
            })

        return house_states

    def execute(self):
        self.cell_model.toggle_entry(self.new_value)

    def undo(self):
        # Restore the original state of the cell
        self.cell_model.value = self.old_value
        self.cell_model.value_type = self.old_value_type
        self.cell_model.notes = self.old_notes[:]
        self.cell_model.notify()

        # Restore the state of all cells in the house
        for state in self.old_house_states:
            state['cell'].model.value = state['value']
            state['cell'].model.value_type = state['value_type']
            state['cell'].model.notes = state['notes'][:]
            state['cell'].model.notify()

        self.board_model.notify()

    def redo(self):
        self.execute()
        self.board_model.notify()


class ToggleNoteCommand(Command):
    def __init__(self, cell_controller, number):
        self.cell_controller = cell_controller
        self.cell_model = cell_controller.model
        self.board_model = cell_controller.board_controller.model
        self.new_value = number
        self.old_value = self.cell_model.value
        self.old_notes = self.cell_model.notes[:]
        self.old_value_type = self.cell_model.value_type

    def execute(self):
        self.cell_model.toggle_note(self.new_value)

    def undo(self):
        self.cell_model.value = self.old_value
        self.cell_model.notes = self.old_notes[:]
        self.cell_model.value_type = self.old_value_type

        self.board_model.notify()
        self.cell_model.notify()

    def redo(self):
        self.execute()
        self.board_model.notify()


class ClearCellCommand(Command):
    def __init__(self, cell_controller):
        self.cell_controller = cell_controller
        self.cell_model = cell_controller.model
        self.board_model = cell_controller.board_controller.model
        self.new_value = None
        self.old_value = self.cell_model.value
        self.old_notes = self.cell_model.notes[:]
        self.old_value_type = self.cell_model.value_type

    def execute(self):
        self.cell_model.clear_cell()

    def undo(self):
        self.cell_model.value = self.old_value
        self.cell_model.notes = self.old_notes[:]
        self.cell_model.value_type = self.old_value_type

        self.board_model.notify()
        self.cell_model.notify()

    def redo(self):
        self.execute()
        self.board_model.notify()
