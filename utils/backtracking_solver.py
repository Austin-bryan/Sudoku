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
        self._solve()
        self.board_controller.view.update()

    def _solve(self):
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True  # No empty cell means the board is solved

        x, y = empty_cell

        for num in range(1, BOARD_SIZE + 1):
            if self._is_safe(x, y, num):
                self._place_number(x, y, num)
                self.iter_count += 1

                self._adjust_update_frequency()

                if self.iter_count % self.step_display == 0:
                    self.board_controller.view.update()
                    time.sleep(0.01)

                if self._solve():
                    return True
                self._remove_number(x, y)
                if self.iter_count % self.step_display == 0:
                    self.board_controller.view.update()

        return False

    def _find_empty_cell(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board_controller.cells[x][y].model.value is None:
                    return x, y
        return None

    def _is_safe(self, x, y, num):
        return (self._is_unused_in_row(x, num) and
                self._is_unused_in_col(y, num) and
                self._is_unused_in_subgrid(x, y, num))

    def _is_unused_in_row(self, x, num):
        for y in range(BOARD_SIZE):
            if self.board_controller.cells[x][y].model.value == num:
                return False
        return True

    def _is_unused_in_col(self, y, num):
        for x in range(BOARD_SIZE):
            if self.board_controller.cells[x][y].model.value == num:
                return False
        return True

    def _is_unused_in_subgrid(self, x, y, num):
        start_x = (x // SUBGRID_SIZE) * SUBGRID_SIZE
        start_y = (y // SUBGRID_SIZE) * SUBGRID_SIZE
        for i in range(start_x, start_x + SUBGRID_SIZE):
            for j in range(start_y, start_y + SUBGRID_SIZE):
                if self.board_controller.cells[i][j].model.value == num:
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
        if elapsed_time > 4.5:
            self.step_display = 100
        if elapsed_time > 4:
            self.step_display = 50
        elif elapsed_time > 3:
            self.step_display = 20
        elif elapsed_time > 2:
            self.step_display = 10
        else:
            self.step_display = 2

