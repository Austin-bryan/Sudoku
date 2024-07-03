import unittest
from models.board_model import BoardModel
from models.cell_model import CellModel
from utils.constants import BOARD_SIZE


class TestBoardModel(unittest.TestCase):
    def setUp(self):
        self.board_model = BoardModel()

    def test_initialization(self):
        """ Tests the initialization of the BoardModel class. """
        self.assertEqual(len(self.board_model.cells), BOARD_SIZE)
        self.assertEqual(len(self.board_model.cells[0]), BOARD_SIZE)

    def test_add_cell_model(self):
        """ Tests the add_cell_model function, ensuring cell models can add themselves to the board model. """
        from models.cell_model import CellModel

        cell_model = CellModel(0, 0)
        self.board_model.add_cell_model(0, 0, cell_model)
        self.assertEqual(self.board_model.cells[0][0], cell_model)

    def test_is_any_selected(self):
        """ Tests is_any_selected returns true if only one cell is selected. """
        self.board_model.cells = [[CellModel(x, y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.assertFalse(self.board_model.is_any_cell_selected())

        self.board_model.cells[0][0].is_selected = True
        self.assertTrue(self.board_model.is_any_cell_selected())


if __name__ == '__main__':
    unittest.main()
