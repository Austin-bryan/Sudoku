import random

from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from utils.backtracking_solver import BacktrackingSolver  # Import your backtracking solver


class SudokuGenerator:
    def __init__(self, board_controller, target_count=40, solver=None):
        self.board_controller = board_controller
        self.solver = BacktrackingSolver(board_controller) if solver is None else solver
        self.target_count = target_count

    def generate_board(self):
        self._empty_board()
        self._fill_board()
        self._remove_numbers()
        self.board_controller.view.update()
        return self.board_controller

    def _empty_board(self):
        for cell in self.board_controller.cells_flat:
            cell.clear()

    def _fill_board(self):
        self.solver.solve()

    def _remove_numbers(self):
        count = self.target_count  # Higher the count, harder the difficulty
        max_iterations = 1000
        iter_count = 0
        non_unique_cache = set()  # Use a set to track cells that cause non-unique solutions

        all_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        random.shuffle(all_cells)  # Shuffle the list to remove cells randomly

        while count > 0 and iter_count < max_iterations:
            if not all_cells:
                break

            i, j = all_cells.pop()
            cell = self.board_controller.cells[i][j]

            if cell in non_unique_cache or cell.model.value is None:
                iter_count += 1
                continue

            old_value = cell.model.value
            cell.model.value = None

            # Always ensure at least 3 cells are removed initially
            if self.target_count - count < 3 or self.solver.has_unique_solution():
                cell.model.value_type = CellValueType.BLANK
                cell.view.update_labels()
                count -= 1
            else:
                cell.model.value = old_value
                non_unique_cache.add(cell)

            iter_count += 1

        # if count > 0:
        #     self._remove_numbers()  # Retry if not enough cells were removed

        # rater = DifficultyRater(self.board_controller)

        # if rater.solve():
        #     self.generate_board()
