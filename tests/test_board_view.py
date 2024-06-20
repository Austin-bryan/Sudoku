import unittest
from tkinter import Tk
from views.board_view import BoardView
from views.cell_view import CellView
from models.cell_model import CellModel


class TestBoardView(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.board_view = BoardView(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertEqual(len(self.board_view.cell_views), 9)
        self.assertEqual(len(self.board_view.cell_views[0]), 9)

    def test_add_cell_view(self):
        cell_model = CellModel(0, 0)
        cell_view = CellView(self.board_view, cell_model)
        self.board_view.add_cell_view(0, 0, cell_view)
        self.assertEqual(self.board_view.cell_views[0][0], cell_view)

    def test_get_frame(self):
        self.assertIsNotNone(self.board_view.get_frame())


if __name__ == '__main__':
    unittest.main()
