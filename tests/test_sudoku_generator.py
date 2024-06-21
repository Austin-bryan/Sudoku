import unittest
import random
from unittest.mock import patch
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from utils.sudoku_generator import SudokuGenerator


class TestSudokuGenerator(unittest.TestCase):
    def setUp(self):
        """ Set up the test environment by initializing the SudokuGenerator. """
        self.generator = SudokuGenerator()

    def test_generate_board(self):
        """ Test that the generate_board method returns a valid Sudoku board. """
        board = self.generator.generate_board()
        self.assertTrue(self._is_valid_sudoku(board))

    def test_fill_diagonal(self):
        """ Test that the fill_diagonal method correctly fills the diagonal boxes. """
        self.generator._fill_diagonal()
        for i in range(0, BOARD_SIZE, SUBGRID_SIZE):
            self.assertTrue(self._is_unique(self.generator.board, i, i))

    def test_fill_box(self):
        """ Test that the fill_box method correctly fills a 3x3 subgrid. """
        self.generator._fill_box(0, 0)
        self.assertTrue(self._is_unique(self.generator.board, 0, 0))

    def test_fill_remaining(self):
        """ Test that the fill_remaining method fills the remaining cells correctly. """
        self.generator._fill_diagonal()
        self.assertTrue(self.generator._fill_remaining(0, SUBGRID_SIZE))
        self.assertTrue(self._is_valid_sudoku(self.generator.board))

    def test_is_safe(self):
        """ Test that the is_safe method correctly identifies safe placements. """
        self.generator.board[0][0] = 5
        self.assertFalse(self.generator._is_safe(0, 1, 5))
        self.assertTrue(self.generator._is_safe(0, 1, 3))

    #
    # Helper Methods for Testing
    #
    def _is_valid_sudoku(self, board):
        """ Helper method to check if a board is a valid Sudoku board. """
        return self._is_valid_rows(board) and self._is_valid_cols(board) and self._is_valid_boxes(board)

    def _is_valid_rows(self, board):
        """ Helper method to check if all rows in a board are valid. """
        for row in board:
            if not self._is_valid_unit(row):
                return False
        return True

    def _is_valid_cols(self, board):
        """ Helper method to check if all columns in a board are valid. """
        for col in zip(*board):
            if not self._is_valid_unit(col):
                return False
        return True

    def _is_valid_boxes(self, board):
        """ Helper method to check if all 3x3 subgrids in a board are valid. """
        for i in range(0, BOARD_SIZE, SUBGRID_SIZE):
            for j in range(0, BOARD_SIZE, SUBGRID_SIZE):
                if not self._is_unique(board, i, j):
                    return False
        return True

    def _is_valid_unit(self, unit):
        """ Helper method to check if a unit (row, column, or subgrid) is valid. """
        unit = [num for num in unit if num != 0]
        return len(unit) == len(set(unit))

    def _is_unique(self, board, start_row, start_col):
        """ Helper method to check if a 3x3 subgrid contains unique numbers. """
        nums = []
        for i in range(SUBGRID_SIZE):
            for j in range(SUBGRID_SIZE):
                num = board[start_row + i][start_col + j]
                if num in nums:
                    return False
                if num != 0:
                    nums.append(num)
        return True


if __name__ == '__main__':
    unittest.main()
