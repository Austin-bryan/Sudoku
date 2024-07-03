import unittest
from tkinter import Tk
from unittest.mock import Mock, MagicMock
import time

from models.cell_model import CellModel
from models.cell_value_type import CellValueType
from controllers.board_controller import BoardController
from undo_history.undo_history_manager import UndoHistoryManager
from utils.constants import BOARD_SIZE
from utils.backtracking_solver import BacktrackingSolver
from utils.sudoku_generator import SudokuGenerator
from views.number_button import NumberButton


class TestBacktrackingSolver(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.board_controller = BoardController(self.root, UndoHistoryManager())
        self.generator = SudokuGenerator(self.board_controller, hint_manager=Mock(), timer=Mock(), solver=Mock(),
                                         target_count=50)

        self.board_controller.cells[0][0].view.update_value_label = Mock()
        self.board_controller.view.update = Mock()
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()
        self.solver = BacktrackingSolver(self.board_controller, True)

    def tearDown(self):
        self.root.update_idletasks()
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_solve_empty_board(self):
        """ Test solving an empty board. """
        for cell in self.board_controller.cells_flat:
            cell.model.value = None

        self.solver.solve()
        self.assertTrue(all(
            cell.model.value is not None
            for cell in self.board_controller.cells_flat
        ))

    def test_solve_almost_solved_board(self):
        """ Test solving a nearly completed board with one empty cell. """
        self.generator.generate_board()
        last_cell = self.board_controller.cells_flat[-1]
        last_cell.model.value = None
        last_cell.model.value_type = CellValueType.BLANK

        self.solver.solve()
        self.assertTrue(last_cell.model.value is not None)

    def test_max_iterations(self):
        """ Test that the solver stops after max_iterations are reached. """
        self.solver.max_iterations = 10
        self.solver.solve()
        self.assertEqual(self.solver.iter_count, 10)

    def test_is_unused_in_house(self):
        """ Test the _is_unused_in_house method. """
        self.board_controller.cells[0][0].get_house = Mock(return_value=[
            self.board_controller.cells[0][1],
            self.board_controller.cells[1][0],
            self.board_controller.cells[1][1]
        ])
        self.board_controller.cells[0][1].model.value = 1
        self.board_controller.cells[1][0].model.value = 2
        self.board_controller.cells[1][1].model.value = 3

        self.assertFalse(self.solver._is_valid_placement(self.board_controller, 0, 0, 1))
        self.assertFalse(self.solver._is_valid_placement(self.board_controller, 0, 0, 2))
        self.assertFalse(self.solver._is_valid_placement(self.board_controller, 0, 0, 3))
        self.assertTrue(self.solver._is_valid_placement(self.board_controller, 0, 0, 4))

    def test_adjust_update_frequency(self):
        """ Test the _adjust_update_frequency method. """
        self.solver.start_time = time.time() - 6
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 200)

        self.solver.start_time = time.time() - 4.75
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 100)

        self.solver.start_time = time.time() - 4.25
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 50)

        self.solver.start_time = time.time() - 3.5
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 20)

        self.solver.start_time = time.time() - 2.5
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 10)

        self.solver.start_time = time.time() - 1.5
        self.solver._adjust_update_frequency()
        self.assertEqual(self.solver.step_display, 2)

    def test_place_number(self):
        """ Test the _place_number method. """
        self.solver._place_number(0, 0, 5)
        self.assertEqual(self.board_controller.cells[0][0].model.value, 5)
        self.assertEqual(self.board_controller.cells[0][0].model.value_type, CellValueType.ENTRY)
        self.board_controller.cells[0][0].view.update_value_label.assert_called_once()

    def test_clear_number(self):
        """ Test the _clear_number method. """
        self.solver._place_number(0, 0, 5)
        self.solver._clear_number(0, 0)
        self.assertIsNone(self.board_controller.cells[0][0].model.value)
        self.board_controller.cells[0][0].view.update_value_label.assert_called()

    def test_has_unique_solution(self):
        """ Ensures the solver is able to detect a board with a unique solution. """
        # Example board with a unique solution
        unique_board_values = [
            [5, 3, None, None, 7, None, None, None, None],
            [6, None, None, 1, 9, 5, None, None, None],
            [None, 9, 8, None, None, None, None, 6, None],
            [8, None, None, None, 6, None, None, None, 3],
            [4, None, None, 8, None, 3, None, None, 1],
            [7, None, None, None, 2, None, None, None, 6],
            [None, 6, None, None, None, None, 2, 8, None],
            [None, None, None, 4, 1, 9, None, None, 5],
            [None, None, None, None, 8, None, None, 7, 9]
        ]

        board_controller = self.create_board_controller(unique_board_values)
        solver = BacktrackingSolver(board_controller)

        self.assertTrue(solver.has_unique_solution(), "Expected the board to have a unique solution")

    def test_has_non_unique_solution(self):
        """ Ensures the solver is able to detect a board with a non-unique solution. """
        # Example board with multiple solutions
        non_unique_board_values = [
            [5, 3, None, None, 7, None, None, None, None],
            [6, None, None, 1, 9, 5, None, None, None],
            [None, 9, 8, None, None, None, None, 6, None],
            [8, None, None, None, 6, None, None, None, 3],
            [4, None, None, 8, None, 3, None, None, 1],
            [7, None, None, None, 2, None, None, None, 6],
            [None, 6, None, None, None, None, 2, 8, None],
            [None, None, None, 4, 1, 9, None, None, 5],
            [None, None, None, None, 8, None, None, None, 9]
        ]

        board_controller = self.create_board_controller(non_unique_board_values)
        solver = BacktrackingSolver(board_controller)

        self.assertFalse(solver.has_unique_solution(), "Expected the board to have multiple solutions")

    #
    # Helper Methods
    #

    @staticmethod
    def create_board_controller(board_values: list[list[int]]):
        """
        Given a 2d list, creates a mock board controller for testing purposes.
        :return: The populated mock board controller.
        """
        board_controller = Mock(spec=BoardController)
        board_controller.cells = []

        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                cell_model = CellModel(x, y)
                cell_model.value = board_values[x][y]
                cell = Mock()
                cell.model = cell_model
                row.append(cell)
            board_controller.cells.append(row)

        return board_controller


if __name__ == '__main__':
    unittest.main()
