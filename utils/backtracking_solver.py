import time
import random

from controllers.board_controller import BoardController
from house_manager import HouseManager
from models.cell_value_type import CellValueType
from utils.Mocks import MockBoard
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from typing import Union


class BacktrackingSolver:
    """
    Solver for the sudoku puzzle.
    Works by placing valid numbers cell by cell, until it reaches a conflict, then it backtracks to the first cell
    where it can try a new value. This goes on until the board is solved.

    Has options to display in UI mode, so we can see the progress, or be instant.
    """

    def __init__(self, board_controller: BoardController, ui_display_mode=False, max_iterations=1000000):
        self.board_controller = board_controller
        self.iter_count = 0  # Counts the number of iterations
        self.step_display = 1  # Used to speed up the display by skipping display numbers
        self.start_time = None
        self.max_iterations = max_iterations  # Used to avoid infinite loops
        self.ui_display_mode = ui_display_mode  # If true, use delays and update the GUI with each step
        self.solutions = 0  # Used to count the number of solutions

    def solve(self) -> bool:
        """
        Sets up the initial conditions for the solving process
        :return: Returns true if it was able to solve the board.
        """
        self.iter_count = 0
        self.step_display = 1
        self.start_time = time.time()
        return self._solve(0, 0)

    def _solve(self, x, y):
        """ Recursively solve the board using backtracking. """
        if self.iter_count >= self.max_iterations:
            return False  # Exceeded maximum allowed iterations
        self.iter_count += 1

        # All cells have been finished
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            return True

        # Move on to the next empty cell
        if self.board_controller.cells[x][y].model.value is not None:
            return self._solve(*self._next_cell(x, y))

        # Shuffle the numbers before trying them
        # This is done for board generation
        numbers = list(range(1, BOARD_SIZE + 1))
        random.shuffle(numbers)
        for num in numbers:
            # Skip to the next valid entry
            if not self._is_valid_placement(self.board_controller, x, y, num):
                continue
            self._place_number(x, y, num)

            # Update GUI to show backtraking solving
            if self.ui_display_mode:
                self._adjust_update_frequency()  # Allows the display to update less and less often
                # Only update the display sometimes
                if self.iter_count % self.step_display == 0:
                    self.board_controller.view.update()
                    time.sleep(0.01)
            if self._solve(*self._next_cell(x, y)):
                return True

            # Backtrack if reached a conflict
            self._clear_number(x, y)
            if self.ui_display_mode and self.iter_count % self.step_display == 0:
                self.board_controller.view.update()
        return False

    def has_unique_solution(self):
        """
        Sets up initial conditions for detecting a unique solution.
        Uses a MockBoard to avoid mutating the actual board.
        """
        board = MockBoard(self.board_controller)
        solutions = []

        if self._check_unique(board, solutions):
            return len(solutions) == 1
        return False

    def _check_unique(self, board: MockBoard, solutions: list[int], x=0, y=0):
        """
        Finds all possible configuration of the board, ensuring that there is only one that has no conflicts.
        :param board: A mock of the board to mutate safely
        :param solutions: used to track solutions found
        :param x: Current X Coordinate
        :param y: Current Y Coordinate
        :return: Whether the board has a unique solution or not.
        """

        # Board is finished
        if x >= BOARD_SIZE:
            solutions.append(1)
            return len(solutions) == 1  # Return True if exactly one solution found

        # Skip to the next empty cell
        if board.cells[x][y].value is not None:
            return self._check_unique(board, solutions, *self._next_cell(x, y))

        # Attempt each number
        for num in range(1, BOARD_SIZE + 1):
            # Ignore invalid numbers
            if not self._is_valid_placement(board, x, y, num):
                continue
            board.cells[x][y].value = num

            if self._check_unique(board, solutions, *self._next_cell(x, y)):
                if len(solutions) > 1:
                    board.cells[x][y].value = None  # Backtrack
                    return False  # More than one solution found
            board.cells[x][y].value = None  # Backtrack

        return len(solutions) == 1  # Return True if exactly one solution found

    @staticmethod
    def _next_cell(x: int, y: int):
        """
        Returns the next right-bottom most cell.

        :param x: Current X Coordinate
        :param y: Current Y Coordinate
        :return: Next cell coordinate
        """
        return (x, y + 1) if y + 1 < BOARD_SIZE else (x + 1, 0)

    def _is_valid_placement(self, board: Union[BoardController, MockBoard], x: int, y: int, num: int):
        """
        Returns true if there are no cells in the house with the value of num.
        :param board: The board controller or MockBoard instance
        :param x: Current X Coordinate
        :param y: Current Y Coordinate
        :param num: The value to check
        :return: Whether num is a valid placement at position (x, y)
        """
        for cell in board.cells[x][y].get_house():
            if cell.value == num:
                return False
        return True

    def _place_number(self, x: int, y: int, num: int):
        """
        Sets the value of the cell model then updates the display.
        This is avoiding using cell.toggle_number() because that involves more steps, such as clearing notes,
        that add overhead in hundreds of iterations.

        :param x: Current X Coordinate
        :param y: Current Y Coordinate
        :param num: The value to place
        """
        cell = self.board_controller.cells[x][y]
        cell.model.value = num
        cell.model.value_type = CellValueType.GIVEN if not self.ui_display_mode else CellValueType.ENTRY
        cell.view.update_value_label()

    def _clear_number(self, x: int, y: int):
        """
        Clears the value, then updates the display.
        This is also avoiding using cell.clear() because that involves more steps, such as clearing notes,
        that add overhead in hundreds of iterations.

        :param x: Current X Coordinate
        :param y: Current Y Coordinate
        """
        cell = self.board_controller.cells[x][y]
        cell.model.value = None
        cell.view.update_value_label()

    def _adjust_update_frequency(self):
        """
        To avoid the display taking too long, this will skip self.step_display amount of iterations to display.
        I've noticed that the solving can range wildly from hundreds of iterations to thousands, so this attempts to
        normalize how long it takes.
        """
        elapsed_time = time.time() - self.start_time

        if elapsed_time > 5:
            self.step_display = 200
        elif elapsed_time > 4.5:
            self.step_display = 100
        elif elapsed_time > 4:
            self.step_display = 50
        elif elapsed_time > 3:
            self.step_display = 20
        elif elapsed_time > 2:
            self.step_display = 10
        else:
            self.step_display = 2
