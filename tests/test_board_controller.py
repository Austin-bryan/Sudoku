import unittest
from unittest.mock import Mock, patch

from controllers.board_controller import BoardController
from tkinter import Tk

from controllers.cell_controller import CellController
from models.board_model import BoardModel
from models.cell_value_type import CellValueType
from observers.conflict_observer import ConflictObserver
from undo_history.undo_history_manager import UndoHistoryManager
from utils.constants import BOARD_SIZE
from views.cell_view import CELL_DEFAULT_COLOR, DefaultCellViewState, SelectedCellViewState, ConflictCellViewState
from views.number_button import NumberButton


class TestBoardController(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.board_controller = BoardController(self.root, UndoHistoryManager())
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        from time import sleep
        self.root.update_idletasks()
        # sleep(0.1)
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

    def test_return_to_default(self):
        """ Ensures that return to default resets all set to a new game, even if they are in conflict. """
        # Simulate a cell with a different state and color
        selected_cell = self.board_controller.cells[0][0]
        other_cell = self.board_controller.cells[0][1]
        selected_cell.select()

        # Ensure that there are cells with different colors initially
        self.assertNotEqual(selected_cell.view.color, other_cell.view.color)
        self.assertTrue(isinstance(selected_cell.view._state_context.state, SelectedCellViewState))
        self.assert_return_to_default()

        self.board_controller.can_select = True
        conflict_observer = ConflictObserver(self.board_controller.model)

        # Ensures returning to default will clear conflicts
        self.setup_cell_conflict(selected_cell)
        self.setup_cell_conflict(other_cell)

        self.assertTrue(selected_cell.model.in_conflict)
        self.assertTrue(isinstance(selected_cell.view._state_context.state, ConflictCellViewState))

        self.assertTrue(other_cell.model.in_conflict)
        self.assertTrue(isinstance(other_cell.view._state_context.state, ConflictCellViewState))

        self.assert_return_to_default()

    #
    # Helper Functions
    #
    def assert_return_to_default(self):
        self.board_controller.return_to_default()

        for cell in self.board_controller.cells_flat:
            self.assertTrue(isinstance(cell.view._state_context.state, DefaultCellViewState))
            self.assertEqual(cell.view.color, CELL_DEFAULT_COLOR)

    def setup_cell_conflict(self, cell):
        cell.model.value_type = CellValueType.ENTRY
        cell.clear()
        cell.toggle_number(1)
        print('val', cell.model.value)


if __name__ == '__main__':
    unittest.main()
