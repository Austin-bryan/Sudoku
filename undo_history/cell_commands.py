from abc import ABC

from undo_history.command import Command
from views.number_button import NumberButton


class CellCommand(Command, ABC):
    def __init__(self, cell_controller):
        self.cell_controller = cell_controller
        self.cell_model = cell_controller.model
        self.board_model = cell_controller.board_controller.model
        self.old_value = self.cell_model.value
        self.old_notes = self.cell_model.notes[:]
        self.old_value_type = self.cell_model.value_type

    def notify_and_update_buttons(self):
        self.board_model.notify()
        NumberButton.show_number_buttons(self.cell_controller)

    def undo(self):
        self.cell_model.value = self.old_value
        self.cell_model.value_type = self.old_value_type
        self.cell_model.notes = self.old_notes[:]
        self.cell_model.notify()
        self.board_model.notify()
        self.cell_controller.select()

    def redo(self):
        self.execute()
        self.cell_controller.select()


class ToggleEntryCommand(CellCommand):
    def __init__(self, cell_controller, number):
        super().__init__(cell_controller)
        self.new_value = number
        self.old_house_states = self._get_house_states()

    def _get_house_states(self):
        house_states = []
        house_cells = self.cell_controller.get_house()
        for cell in house_cells:
            house_states.append({
                'cell': cell,
                'value': cell.model.value,
                'notes': cell.model.notes[:],
                'value_type': cell.model.value_type
            })
        return house_states

    def execute(self):
        self.cell_controller.reset_matching_cells()
        self.cell_model.toggle_entry(self.new_value)
        for cell in self.cell_controller.get_house():
            if cell.model.is_notes() and cell.model.has_note(self.new_value):
                cell.model.toggle_note(self.new_value)
        self.notify_and_update_buttons()

    def undo(self):
        super().undo()
        for state in self.old_house_states:
            state['cell'].model.value = state['value']
            state['cell'].model.value_type = state['value_type']
            state['cell'].model.notes = state['notes'][:]
            state['cell'].model.notify()


class ToggleNoteCommand(CellCommand):
    def __init__(self, cell_controller, number):
        super().__init__(cell_controller)
        self.new_value = number

    def execute(self):
        self.cell_model.toggle_note(self.new_value)
        self.notify_and_update_buttons()


class ClearCellCommand(CellCommand):
    def execute(self):
        self.cell_controller.reset_matching_cells()
        self.cell_model.clear_cell()
        self.notify_and_update_buttons()

    def undo(self):
        super().undo()
        self.cell_controller.highlight_house()
