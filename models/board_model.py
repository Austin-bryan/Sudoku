from models.cell_model import CellModel
from models.subject import Subject
from utils.constants import BOARD_SIZE


class BoardModel(Subject):
    """ Contains the data and cell models for the Board Controller class. """
    def __init__(self):
        super().__init__()
        self.cells: list[list['CellModel']] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def populate_board(self, numbers):
        """ Assigns the cell models with the given numbers. """
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if numbers[x][y] != 0:
                    self.cells[x][y].set_given(numbers[x][y])

    def get_cell_value(self, x: int, y: int) -> int:
        """
        Returns the value of the cell at the x and y coordinates.
        :param x: X coordinate of the cell.
        :param y: Y coordinate of the cell.
        """
        return self.cells[x][y].value

    def add_cell_model(self, x: int, y: int, cell_model):
        """
        Used by cell models when they are created to add themselves to the board.

        :param x: X coordinate of the cell.
        :param y: Y coordinate of the cell.
        :param cell_model: The cell model to add.
        """
        self.cells[x][y] = cell_model

    def is_any_cell_selected(self) -> bool:
        """
        Returns true if any cell model is selected.
        This is used to determine if the user has started playing the game.
        Once a cell is selected, there is no mechanism to unselect all cells other than beating the game.
        """
        for row in self.cells:
            for cell in row:
                if cell.is_selected:
                    return True
        return False
