import random

from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from utils.backtracking_solver import BacktrackingSolver  # Import your backtracking solver


class SudokuGenerator:
    def __init__(self, board_controller):
        self.board_controller = board_controller
        self.solver = BacktrackingSolver(board_controller, generate_mode=True)

    def generate_board(self):
        self._fill_board()
        self._remove_numbers()
        self.board_controller.view.update()
        return self.board_controller

    def _fill_board(self):
        self.solver.solve()

    def _remove_numbers(self):
        count = 10  # Adjust this for difficulty
        while count > 0:
            i = random.randint(0, BOARD_SIZE - 1)
            j = random.randint(0, BOARD_SIZE - 1)
            while self.board_controller.cells[i][j].model.value is None:
                i = random.randint(0, BOARD_SIZE - 1)
                j = random.randint(0, BOARD_SIZE - 1)
            # Backup the value
            self.board_controller.cells[i][j].model.value = None
            self.board_controller.cells[i][j].model.value_type = CellValueType.BLANK
            self.board_controller.cells[i][j].view.update_labels()
            count -= 1

    def _can_solve(self):
        from controllers.board_controller import BoardController
        # Create a new solver instance with a copy of the board
        temp_board = [[cell for cell in row] for row in self.board_controller.cells]
        temp_controller = BoardController(self.board_controller.parent)
        temp_controller.cells = temp_board
        solver = BacktrackingSolver(temp_controller)
        return solver.solve()
