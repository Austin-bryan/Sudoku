import random

from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from utils.backtracking_solver import BacktrackingSolver  # Import your backtracking solver


class SudokuGenerator:
    def __init__(self, board_controller, target_count=40):
        self.board_controller = board_controller
        self.solver = BacktrackingSolver(board_controller)
        self.target_count = target_count

    def generate_board(self):
        self._fill_board()
        self._remove_numbers()
        self.board_controller.view.update()
        return self.board_controller

    def _fill_board(self):
        self.solver.solve()

    def _remove_numbers(self):
        count = self.target_count  # Higher the count, harder the difficulty
        max_iterations = 100
        iter_count = 0
        solver = BacktrackingSolver(self.board_controller)
        non_unique_cache = []  # These are cells that once removed, prevent a unique solution from existing

        def get_cell():
            i = random.randint(0, BOARD_SIZE - 1)
            j = random.randint(0, BOARD_SIZE - 1)
            return self.board_controller.cells[i][j]

        while count > 0:
            cell = get_cell()
            while cell.model.value is None:
                iter_count += 1
                if iter_count > max_iterations:
                    count = 0
                    break
                cell = get_cell()

            old_value = cell.model.value
            cell.model.value = None

            if solver.has_unique_solution():
                cell.model.value_type = CellValueType.BLANK
                cell.view.update_labels()

                count -= 1
            else:
                cell.model.value = old_value
                non_unique_cache.append(cell)
        print(solver.has_unique_solution())
