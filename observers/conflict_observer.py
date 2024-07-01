from enum import Enum

from models.board_model import BoardModel
from models.cell_model import CellModel
from observers.observer import Observer
from utils.constants import BOARD_SIZE


class ConflictObserver(Observer):
    """ Observes the board model, and gets notified on changes. It uses this to detect conflicts. """
    def __init__(self, board_model: BoardModel):
        self.board_model = board_model
        self.board_model.attach(self)

    def update(self):
        """ Executes the detect conflicts method. """
        self.detect_conflicts()

    def detect_conflicts(self):
        """ Loops through each coordinate, updating the conflict status based on whether a conflict exists. """
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                cell_model = self.board_model.cells[x][y]
                cell_model.set_conflict_status(self.has_conflict(cell_model, cell_model.get_house()))

    @staticmethod
    def has_conflict(cell_model: CellModel, house: list[CellModel]) -> bool:
        """
        Given a cell model and a house, determines if a conflict exists.
        A conflict exists if two cells in the same house have the same value. Notes do not count towards this.
        :param cell_model: The cell to check
        :param house: The house of the model to check
        :return: Whether the conflict exists
        """

        # Get all values in cell, ignoring 0 or None
        values = [cell.value for cell in house if cell.value != 0 and cell.value is not None]
        for value in values:
            if value == cell_model.value:
                return True
        return False
