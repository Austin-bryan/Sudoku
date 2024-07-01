import unittest
from unittest.mock import Mock

from utils.Mocks import MockCell


class TestMockCell(unittest.TestCase):
    def setUp(self):
        self.cell = MockCell(0, 0, 0 , Mock())

    def test_row(self):
        self.cell.house_manager.get_row = Mock()
        self.cell.get_row()
        self.cell.house_manager.get_row.assert_called_once()

    def test_column(self):
        self.cell.house_manager.get_column = Mock()
        self.cell.get_column()
        self.cell.house_manager.get_column.assert_called_once()

    def test_subgrid(self):
        self.cell.house_manager.get_subgrid = Mock()
        self.cell.get_subgrid()
        self.cell.house_manager.get_subgrid.assert_called_once()

    def test_house(self):
        self.cell.house_manager.get_house = Mock()
        self.cell.get_house()
        self.cell.house_manager.get_house.assert_called_once()


if __name__ == '__main__':
    unittest.main()
