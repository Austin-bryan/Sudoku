import random

from controllers.board_controller import BoardController
from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from utils.backtracking_solver import BacktrackingSolver  # Import your backtracking solver


class SudokuGenerator:
    """ Generates a sudoku puzzle that has only one unique solution. """

    def __init__(self, board_controller: BoardController, target_count=40, solver: BacktrackingSolver=None):
        self.board_controller = board_controller
        self.solver = BacktrackingSolver(board_controller) if solver is None else solver
        self.target_count = target_count

    def generate_board(self):
        """" Generates a board, randomly removes numbers, then updates the views. """
        self._empty_board()
        self._fill_board()
        self._remove_numbers()
        self.board_controller.view.update()

    def _empty_board(self):
        """ Clears all cells. """
        for cell in self.board_controller.cells_flat:
            cell.clear()

    def _fill_board(self):
        """
        Fills the board by solving an empty board.
        The solver uses randomization to avoid creating the same board every time.
        """
        self.solver.solve()

    def _remove_numbers(self):
        """
        Randomly removes numbers from the board to create the puzzle.
        Amount removed is determined by difficulty.
        """
        number_cells_to_remove = self.target_count  # Higher the count, harder the difficulty
        max_iterations = 1000
        iterations = 0
        non_unique_cache = set()  # Use a set to track cells that cause non-unique solutions

        all_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        random.shuffle(all_cells)  # Shuffle the list to remove cells randomly

        # Remove until count is reached
        while number_cells_to_remove > 0 and iterations < max_iterations:
            if not all_cells:
                break

            i, j = all_cells.pop()
            cell = self.board_controller.cells[i][j]

            # Don't remove cells that previously allowed multiple solutions when removed
            if cell in non_unique_cache or cell.model.value is None:
                iterations += 1
                continue

            # Cache value before assigning to None, in case we need to restore it
            old_value = cell.model.value
            cell.model.value = None

            # Always ensure at least 3 cells are removed initially
            if self.target_count - number_cells_to_remove < 3 or self.solver.has_unique_solution():
                # Unique solution exists, finalize removal
                cell.model.value_type = CellValueType.BLANK
                cell.view.update_labels()
                number_cells_to_remove -= 1
            else:
                # Lost unique solution, revert changes and cache number
                cell.model.value = old_value
                non_unique_cache.add(cell)

            iterations += 1
