from models.cell_model import CellModel
from models.subject import Subject
from utils.constants import BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator


class BoardModel(Subject):
    def __init__(self):
        super().__init__()
        self.cells: list[list['CellModel']] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def populate_board(self, numbers):
        """ Assigns the cell models with the given numbers. """
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if numbers[x][y] != 0:
                    self.cells[x][y].set_given(numbers[x][y])

    def get_cell_value(self, x, y):
        return self.cells[x][y].value

    def add_cell_model(self, x, y, cell_model):
        """ Used by cell models when they are created to add themselves to the board. """
        self.cells[x][y] = cell_model
