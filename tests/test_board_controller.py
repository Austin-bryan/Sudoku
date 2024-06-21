import unittest
from unittest.mock import Mock

from controllers.board_controller import BoardController
from tkinter import Tk

from utils.constants import BOARD_SIZE
from views.number_button import NumberButton


class TestBoardController(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.board_controller = BoardController(self.root)
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_initialization(self):
        self.assertEqual(len(self.board_controller.cells), BOARD_SIZE)
        self.assertEqual(len(self.board_controller.cells[0]), BOARD_SIZE)

    def test_populate_board(self):
        numbers = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        numbers[0][0] = 5
        self.board_controller.populate_board(numbers)
        self.assertEqual(self.board_controller.model.get_cell_value(0, 0), 5)

    def test_cells_flat(self):
        self.assertEqual(len(self.board_controller.cells_flat), BOARD_SIZE ** 2)

    def test_clear_selected(self):
        cell_controller = self.board_controller.cells[0][0]
        cell_controller.model.set_given(5)
        self.board_controller.selected_cell = cell_controller

        self.board_controller.clear_selected()
        self.assertEqual(cell_controller.model.value, 5)  # Given value should not be cleared

    def test_toggle_selected_cell(self):
        cell_controller = self.board_controller.cells[0][0]
        self.board_controller.selected_cell = cell_controller
        self.board_controller.toggle_selected_cell(5)
        self.assertEqual(cell_controller.model.value, 5)

    def test_get_frame(self):
        self.assertIsNotNone(self.board_controller.get_frame())


if __name__ == '__main__':
    unittest.main()
