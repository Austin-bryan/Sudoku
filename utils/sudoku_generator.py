import random

from controllers.board_controller import BoardController
from controllers.cell_controller import CellController
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
            iterations += 1

            if not all_cells:
                break

            i, j = all_cells.pop()
            cell = self.board_controller.cells[i][j]

            sym_cells = self._get_symmetrical_cells(cell)

            # Don't remove cells that previously allowed multiple solutions when removed
            if cell in non_unique_cache or cell.model.value is None:
                continue

            # Skip blank cells
            if all(c.model.value is None for c in sym_cells):
                continue

            # Cache values before assigning to None, in case we need to restore it
            old_values = [c.model.value for c in sym_cells]
            for c in sym_cells:
                c.model.value = None

            if self.solver.has_unique_solution():
                # Unique solution exists, finalize removal
                number_cells_to_remove -= len(sym_cells)
                for c in sym_cells:
                    c.model.value_type = CellValueType.BLANK
                    c.view.update_labels()
            else:
                # Unique solution not found, undo removal
                for c, val in zip(sym_cells, old_values):
                    c.model.value = val

    def _get_symmetrical_cells(self, cell: CellController):
        """
        Gets the 3 symmetrical cells from the given cell.
        :param cell: The cell to get symmetrical cells from.
        :return: A list of 4 cells that are 4 way symmetrical.
        """
        x, y = cell.model.x, cell.model.y
        return [
            self.board_controller.cells[x][y],
            self.board_controller.cells[BOARD_SIZE - 1 - x][y],
            self.board_controller.cells[x][BOARD_SIZE - 1 - y],
            self.board_controller.cells[BOARD_SIZE - 1 - x][BOARD_SIZE - 1 - y]
        ]