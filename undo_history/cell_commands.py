from abc import ABC

from controllers.cell_controller import CellController
from undo_history.command import Command
from views.number_button import NumberButton


class CellCommand(Command, ABC):
    """
    Base class for cell commands, such as Toggle Entry, Toggle Note, and Clear.
    The use of the command pattern allows easy undoing and redoing.
    """
    def __init__(self, cell_controller: CellController):
        self.cell_controller = cell_controller
        self.cell_model = cell_controller.model
        self.board_model = cell_controller.board_controller.model
        self.old_value = self.cell_model.value
        self.old_notes = self.cell_model.notes[:]
        self.old_value_type = self.cell_model.value_type

    def notify_and_update_buttons(self):
        """ Update and notify when a change is made. """
        self.board_model.notify()
        NumberButton.show_number_buttons(self.cell_controller)

    def undo(self):
        """ Restores the cell command to all cached values, then notify everything. """
        self.cell_model.value = self.old_value
        self.cell_model.value_type = self.old_value_type
        self.cell_model.notes = self.old_notes[:]
        self.cell_model.notify()
        self.board_model.notify()
        self.cell_controller.select()

    def redo(self):
        """ Restores the cell command to all cached values, then notify everything. """
        self.execute()
        self.cell_controller.select()


class ToggleEntryCommand(CellCommand):
    """ Command for when the user toggles an entry on or off. """
    def __init__(self, cell_controller: CellController, number: int):
        """
        :param cell_controller: Controller for the cell this command effects
        :param number: The number being toggled on or off
        """
        super().__init__(cell_controller)
        self.new_value = number
        self.old_house_states = self._get_house_states()

    def _get_house_states(self):
        """ Stores all information from each state to restore later. """
        house_states = []
        house_cells = self.cell_controller.get_house()

        # Since execute removes notes from all cells in house, it is important to cache the entire house, so undoing
        # will undo the side effects of toggling.
        for cell in house_cells:
            house_states.append({
                'cell': cell,
                'value': cell.model.value,
                'notes': cell.model.notes[:],
                'value_type': cell.model.value_type
            })
        return house_states

    def execute(self):
        """ Toggles entry on or off, and updates UI display. """
        self.cell_controller.reset_matching_cells()
        self.cell_model.toggle_entry(self.new_value)

        # Remove notes of with the number being toggled on in house
        for cell in self.cell_controller.get_house():
            if cell.model.is_notes() and cell.model.has_note(self.new_value):
                cell.model.toggle_note(self.new_value)
        self.notify_and_update_buttons()

    def undo(self):
        """ Restores state of not just the cell controller, but of all cells in the house. """
        super().undo()
        for state in self.old_house_states:
            state['cell'].model.value = state['value']
            state['cell'].model.value_type = state['value_type']
            state['cell'].model.notes = state['notes'][:]
            state['cell'].model.notify()


class ToggleNoteCommand(CellCommand):
    """ Enables toggling of a note on or off. """
    def __init__(self, cell_controller: CellController, number: int):
        super().__init__(cell_controller)
        self.new_value = number

    def execute(self):
        """ Toggles note on or off, and updates UI display. """
        self.cell_model.toggle_note(self.new_value)
        self.notify_and_update_buttons()


class ClearCellCommand(CellCommand):
    """ Clears the cell, removing both entries and notes in one command. """
    def execute(self):
        """ Clears the cell and updates UI display. """
        self.cell_controller.reset_matching_cells()
        self.cell_model.clear()
        self.notify_and_update_buttons()

    def undo(self):
        """ Restores the value and any possible cached notes that weren't visible. """
        super().undo()
        self.cell_controller.highlight_house()
