import time
import tkinter as tk
from unittest.mock import Mock

from controllers.board_controller import BoardController
from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from views.number_button import NumberButton


class BacktrackingSolver:

    def __init__(self, board_controller):
        self.board_controller = board_controller
        self.iter_count = 0
        self.step_display = 1
        self.start_time = None

    def solve(self):
        self.iter_count = 0
        self.step_display = 1
        NumberButton.show_number_buttons = Mock()
        self.start_time = time.time()
        self._solve(0, 0)
        self.board_controller.view.update()

    def _solve(self, x, y):
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            return True  # Reached the end of the board, the puzzle is solved

        if self.board_controller.cells[x][y].model.value is not None:
            return self._solve(*self._next_cell(x, y))
        for num in range(1, BOARD_SIZE + 1):
            if not self._is_unused_in_house(x, y, num):
                continue
            self._place_number(x, y, num)
            self.iter_count += 1

            self._adjust_update_frequency()

            if self.iter_count % self.step_display == 0:
                self.board_controller.view.update()
                time.sleep(0.01)

            if self._solve(*self._next_cell(x, y)):
                return True
            self._remove_number(x, y)
            if self.iter_count % self.step_display == 0:
                self.board_controller.view.update()
        return False

    @staticmethod
    def _next_cell(x, y):
        return (x, y + 1) if y + 1 < BOARD_SIZE else (x + 1, 0)

    def _is_unused_in_house(self, x, y, num):
        for cell in self.board_controller.cells[x][y].get_house():
            if cell.model.value == num:
                return False
        return True

    def _place_number(self, x, y, num):
        cell = self.board_controller.cells[x][y]
        cell.model.value = num
        cell.model.value_type = CellValueType.ENTRY
        cell.view.update_entry_label()

    def _remove_number(self, x, y):
        cell = self.board_controller.cells[x][y]
        cell.model.value = None
        cell.view.update_entry_label()

    def _adjust_update_frequency(self):
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
