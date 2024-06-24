import time
import random

from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE


class BacktrackingSolver:

    def __init__(self, board_controller, generate_mode=False, max_iterations=1000000):
        self.board_controller = board_controller
        self.iter_count = 0  # Counts the number of iterations
        self.step_display = 1  # Used to speed up the display by skipping display numbers
        self.start_time = None
        self.max_iterations = max_iterations
        self.generate_mode = generate_mode

    def solve(self):
        self.iter_count = 0
        self.step_display = 1
        self.start_time = time.time()
        self._solve(0, 0)

    def _solve(self, x, y):
        """ Recursively solve the board using backtracking. """
        if self.iter_count >= self.max_iterations:
            return False  # Exceeded maximum allowed iterations
        self.iter_count += 1

        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            return True  # Reached the end of the board, the puzzle is solved

        if self.board_controller.cells[x][y].model.value is not None:
            return self._solve(*self._next_cell(x, y))  # Move on to the next empty cell

        numbers = list(range(1, BOARD_SIZE + 1))
        random.shuffle(numbers)  # Shuffle the numbers before trying them
        for num in numbers:
            if not self._is_unused_in_house(x, y, num):  # Skip to the next valid entry
                continue
            self._place_number(x, y, num)

            if not self.generate_mode:
                self._adjust_update_frequency()  # Allows the display to update less and less often

                # Only update the display sometimes
                if self.iter_count % self.step_display == 0:
                    self.board_controller.view.update()
                    time.sleep(0.01)

            if self._solve(*self._next_cell(x, y)):
                return True

            # Backtrack
            self._clear_number(x, y)
            if not self.generate_mode and self.iter_count % self.step_display == 0:
                self.board_controller.view.update()
        return False

    @staticmethod
    def _next_cell(x, y):
        """ Returns the next right-bottom most cell. """
        return (x, y + 1) if y + 1 < BOARD_SIZE else (x + 1, 0)

    def _is_unused_in_house(self, x, y, num):
        """ Returns true if there are no cells in the house with the value of num. """
        for cell in self.board_controller.cells[x][y].get_house():
            if cell.model.value == num:
                return False
        return True

    def _place_number(self, x, y, num):
        """
        Sets the value of the cell model then updates the display.
        This is avoiding using cell.toggle_number() because that involves more steps, such as clearing notes,
        that add overhead in hundreds of iterations.
        """
        cell = self.board_controller.cells[x][y]
        cell.model.value = num
        cell.model.value_type = CellValueType.GIVEN if self.generate_mode else CellValueType.ENTRY
        cell.view.update_value_label()

    def _clear_number(self, x, y):
        """
        Clears the value, then updates the display.
        This is also avoiding using cell.clear() because that involves more steps, such as clearing notes,
        that add overhead in hundreds of iterations.
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
