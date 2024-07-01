from models.cell_value_type import CellValueType
from models.subject import Subject
from utils.constants import BOARD_SIZE


class CellModel(Subject):
    """ Handles all the data for the cell controller, including value, notes, and various states. """
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x, self.y = x, y
        self.value, self.notes = None, [False] * BOARD_SIZE
        self.in_conflict = False
        self.is_selected = False
        self.value_type = CellValueType.BLANK
        self.house_manager = None

    def toggle_entry(self, number: int):
        """
        Toggles an entry on or off.
        Notes are not cleared during this process, so that they can be restored again later by toggling off the number.

        :param number: The number to toggle as an entry
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
        """
        Once a cell is set to given, it can never be changed by the user to another cell value type.
        It can be changed when creating a new game.
        """
        self.value = number
        self.value_type = CellValueType.GIVEN
        self.notify()

    def clear(self):
        """ Clears all contents of the cell, both value and all notes. Sets the state back to BLANK. """
        if self.is_given():
            return
        self.value = None
        self.in_conflict = False
        self.notes = [False] * BOARD_SIZE
        self.value_type = CellValueType.BLANK
        self.notify()

    def toggle_note(self, number):
        """
        Turns a note on or off. Multiple notes can be on at once.
        :param number: The number to toggle as an note
        """
        if self.is_given():
            return
        self.value = None
        self.notes[number - 1] = not self.notes[number - 1]
        self.value_type = CellValueType.NOTES if any(self.notes) else CellValueType.BLANK
        self.notify()

    def set_conflict_status(self, state):
        """
        Updates the conflict status of the cell, then notifies observers.
        :param state:
        """
        self.in_conflict = state
        self.notify()

    def is_entry(self) -> bool:
        """
        Returns true if the user has entered their own value in this cell.
        It is possible for a cell to have cached notes that are not displayed, but a value is displayed.
        This will return true in that instance.
        """
        return self.value_type == CellValueType.ENTRY

    def is_given(self) -> bool:
        """ Returns true fit the this cell was a given clue and cannot be changed by the user. """
        return self.value_type == CellValueType.GIVEN

    def is_notes(self) -> bool:
        """ Returns true if cell has at least one active note. It's possible to have multiple active notes. """
        return self.value_type == CellValueType.NOTES

    def is_blank(self) -> bool:
        return self.value_type == CellValueType.BLANK

    def has_value(self) -> bool:
        return self.value is not None

    def has_note(self, number) -> bool:
        """ Returns true if the cell has the note of the specified number active. """
        return self.notes[number - 1]

    def get_house(self) -> list['CellModel']:
        """ Returns the cell models in the same house (row, column and subgrid) as self. """
        return self.house_manager.get_house()

    def get_row(self) -> list['CellModel']:
        """ Returns the cell models in the same row as self. """
        return self.house_manager.get_row()

    def get_column(self) -> list['CellModel']:
        """ Returns the cell models in the same column as self. """
        return self.house_manager.get_column()

    def get_subgrid(self) -> list['CellModel']:
        """ Returns the cell models in the same subgrid as self. """
        return self.house_manager.get_subgrid()


def get_possible_values(cell: CellModel) -> set[int]:
    """
    Returns all possible values for a cell. These are the numbers that are no where else found in the house.
    If this returns an empty list, then a conflict must exist somewhere.
    :param cell: The cell to get the possible values of.
    """
    possible_values = set(range(1, BOARD_SIZE + 1))
    used_values = {c.value for c in cell.get_house() if c.value is not None}
    return possible_values - used_values
