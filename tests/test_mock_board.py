import unittest
from unittest.mock import Mock
from controllers.board_controller import BoardController
from models.cell_model import CellModel
from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE
from utils.Mocks import MockBoard  # Ensure this import matches your file structure


class TestMockBoard(unittest.TestCase):
    def setUp(self):
        self.board_controller = Mock(spec=BoardController)
        self.board_controller.cells = []

        # Populate the mock board controller with mock cells
        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                cell_model = Mock(spec=CellModel)
                cell_model.value = (x * BOARD_SIZE + y) % 9 + 1  # Some test values
                cell_model.value_type = CellValueType.GIVEN
                cell = Mock()
                cell.model = cell_model
                row.append(cell)
            self.board_controller.cells.append(row)

    def test_mock_board_initialization(self):
        mock_board = MockBoard(self.board_controller)

        # Check if the mock_board cells have the same values as the board_controller cells
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                original_value = self.board_controller.cells[x][y].model.value
                mock_value = mock_board.cells[x][y].value
                self.assertEqual(original_value, mock_value, f"Mismatch at ({x}, {y}): {original_value} != {mock_value}")


if __name__ == '__main__':
    unittest.main()