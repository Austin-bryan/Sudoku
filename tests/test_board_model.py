import unittest
from models.board_model import BoardModel
from utils.constants import BOARD_SIZE


class TestBoardModel(unittest.TestCase):
    def setUp(self):
        self.board_model = BoardModel()

    def test_initialization(self):
        self.assertEqual(len(self.board_model.cell_models), BOARD_SIZE)
        self.assertEqual(len(self.board_model.cell_models[0]), BOARD_SIZE)

    def test_add_cell_model(self):
        from models.cell_model import CellModel

        cell_model = CellModel(0, 0)
        self.board_model.add_cell_model(0, 0, cell_model)
        self.assertEqual(self.board_model.cell_models[0][0], cell_model)


if __name__ == '__main__':
    unittest.main()
