import unittest
from tkinter import Tk

from utils.constants import BOARD_SIZE
from views.board_view import BoardView
from views.cell_view import CellView
from models.cell_model import CellModel


class TestBoardView(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.board_view = BoardView(self.root)

    def tearDown(self):
        self.root.update_idletasks()
        self.root.destroy()

    def test_initialization(self):
        """ Tests the initialization of the BoardView. """
        self.assertEqual(len(self.board_view.cells), BOARD_SIZE)
        self.assertEqual(len(self.board_view.cells[0]), BOARD_SIZE)

    def test_add_cell_view(self):
        """ Ensures that cell views can add themselves to the board view. """
        cell_model = CellModel(0, 0)
        cell_view = CellView(self.board_view, cell_model)
        self.board_view.add_cell_view(0, 0, cell_view)
        self.assertEqual(self.board_view.cells[0][0], cell_view)


if __name__ == '__main__':
    unittest.main()
