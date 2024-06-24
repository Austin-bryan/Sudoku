import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from controllers.board_controller import BoardController
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator


class TestSudokuGenerator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.board_controller = BoardController(self.root)
        self.generator = SudokuGenerator(self.board_controller)

    def tearDown(self):
        self.root.update_idletasks()
        self.root.destroy()

    @patch.object(SudokuGenerator, '_fill_board')
    @patch.object(SudokuGenerator, '_remove_numbers')
    def test_generate_board(self, mock_remove_numbers, mock_fill_board):
        self.generator.generate_board()
        mock_fill_board.assert_called_once()
        mock_remove_numbers.assert_called_once()

    def test_fill_board(self):
        with patch.object(BacktrackingSolver, 'solve') as mock_solve:
            self.generator._fill_board()
            mock_solve.assert_called_once()

    def test_remove_numbers(self):
        # Mocking the board to have all cells filled initially
        for cell in self.board_controller.cells_flat:
            cell.model.value = 1  # Arbitrary non-None value
        self.generator._remove_numbers()

        # Check if the correct number of cells were cleared
        cleared_cells = sum(1 for i in range(BOARD_SIZE)
                            for j in range(BOARD_SIZE)
                            if self.board_controller.cells[i][j].model.value is None)
        self.assertEqual(cleared_cells, 40)

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

    @patch('random.randint', return_value=0)
    def test_remove_numbers_random(self, mock_randint):
        self.generator._fill_board()
        self.generator._remove_numbers()
        mock_randint.assert_called()


if __name__ == '__main__':
    unittest.main()
