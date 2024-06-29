import random
from abc import ABC, abstractmethod

from models.cell_value_type import CellValueType
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BOARD_SIZE


class Difficulty(ABC):
    def __init__(self, board_controller, target_count):
        self.board_controller = board_controller
        self._solver = BacktrackingSolver(board_controller)
        self.target_count = target_count

    @abstractmethod
    def remove_cells(self):
        pass


class EasyDifficulty(Difficulty):
    def __init__(self, board_controller):
        super().__init__(board_controller, 40)

    def remove_cells(self):
        count = self.target_count  # Higher the count, harder the difficulty
        max_iterations = 1000
        iter_count = 0
        non_unique_cache = []  # These are cells that once removed, prevent a unique solution from existing

        def get_cell():
            i = random.randint(0, BOARD_SIZE - 1)
            j = random.randint(0, BOARD_SIZE - 1)
            return self.board_controller.cells[i][j]

        while count > 0:
            cell = get_cell()
            while cell.model.value is None and cell in non_unique_cache:
                iter_count += 1
                if iter_count > max_iterations:
                    count = 0
                    break
                cell = get_cell()

            old_value = cell.model.value
            cell.model.value = None

            if self._solver.has_unique_solution():
                cell.model.value_type = CellValueType.BLANK
                cell.view.update_labels()

                count -= 1
            else:
                cell.model.value = old_value
                non_unique_cache.append(cell)


