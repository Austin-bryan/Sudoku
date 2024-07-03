import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock, Mock
from controllers.board_controller import BoardController
from undo_history.undo_history_manager import UndoHistoryManager
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator
from views.number_button import NumberButton


class TestSudokuGenerator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.board_controller = BoardController(self.root, UndoHistoryManager())
        self.generator = SudokuGenerator(self.board_controller, hint_manager=Mock(), timer=Mock(), solver=Mock(),
                                         target_count=50)
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        from time import sleep
        self.root.update_idletasks()
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    @patch.object(SudokuGenerator, '_fill_board')
    @patch.object(SudokuGenerator, '_remove_numbers')
    def test_generate_board(self, mock_remove_numbers, mock_fill_board):
        self.generator.generate_board()
        mock_fill_board.assert_called_once()
        mock_remove_numbers.assert_called_once()

    # def test_fill_board(self):
    #     with patch.object(BacktrackingSolver, 'solve') as mock_solve:
    #         self.generator._fill_board()
    #         mock_solve.assert_called_once()

    def test_remove_numbers(self):
        """ Tests that removing cells removes in the correct range of numbers. """
        # Mocking the board to have all cells filled initially
        for cell in self.board_controller.cells_flat:
            cell.model.value = 1  # Arbitrary non-None value

        solver = BacktrackingSolver(self.board_controller)
        solver.has_unique_solution = Mock(return_value=True)
        self.generator = SudokuGenerator(self.board_controller, hint_manager=Mock(), timer=Mock(), solver=solver,
                                         target_count=50)
        self.generator._remove_numbers()

        # Check if the correct number of cells were cleared
        cleared_cells = sum(1 for i in range(BOARD_SIZE)
                            for j in range(BOARD_SIZE)
                            if self.board_controller.cells[i][j].model.value is None)

        # Since cells are removed 4 at a time to maintain symmetry, this can allow for variance,
        # Removing either 2 or only 1 is possible if the cell is in the middle or direct center.
        # This check tries to account for that
        min_cleared_cells = (self.generator.target_count // 4)
        self.assertTrue(min_cleared_cells <= cleared_cells <= self.generator.target_count)

    def test_remove_numbers_bounds(self):
        # Check if _remove_numbers handles empty and full boards correctly
        self.generator._remove_numbers()  # Empty board case
        self.generator._fill_board()
        self.generator._remove_numbers()  # Full board case

        # Ensure no out-of-bounds access
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.board_controller.cells[i][j]
                self.assertTrue(0 <= i < BOARD_SIZE)
                self.assertTrue(0 <= j < BOARD_SIZE)

    @patch('random.shuffle')
    def test_remove_numbers_random(self, mock_random_shuffle):
        self.generator._fill_board()
        self.generator._remove_numbers()
        mock_random_shuffle.assert_called()


if __name__ == '__main__':
    unittest.main()
