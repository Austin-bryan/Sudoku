import unittest
from unittest.mock import Mock

from models.cell_model import CellModel, get_possible_values
from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE


class TestCellModel(unittest.TestCase):
    def setUp(self):
        self.cell_model = CellModel(0, 0)

    def test_init(self):
        """ Asserts the initial state of the cell model."""
        self.assertEqual(self.cell_model.x, 0)
        self.assertEqual(self.cell_model.y, 0)
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.notes, [False for _ in range(BOARD_SIZE)])
        self.assertFalse(self.cell_model.in_conflict)
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_toggle_entry(self):
        """ Asserts that toggling an entry on and off works."""
        self.cell_model.toggle_entry(5)
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

        self.cell_model.toggle_entry(5)
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_toggle_entry_given(self):
        """ Tests that toggling entries have no effect on a given."""
        self.cell_model.set_given(7)
        self.cell_model.toggle_entry(5)
        self.assertEqual(self.cell_model.value, 7)
        self.assertEqual(self.cell_model.value_type, CellValueType.GIVEN)

    def test_set_given(self):
        """ Tests that setting the given sets the value and value type properly."""
        self.cell_model.set_given(8)
        self.assertEqual(self.cell_model.value, 8)
        self.assertEqual(self.cell_model.value_type, CellValueType.GIVEN)

    def test_toggle_note(self):
        """ Assures that toggling notes on and off works."""
        self.cell_model.toggle_note(3)
        self.assertTrue(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

        self.cell_model.toggle_note(3)
        self.assertFalse(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_clear(self):
        """ Asserts that clear removes all notes and entry"""
        self.cell_model.toggle_entry(3)
        self.cell_model.toggle_note(2)
        self.cell_model.toggle_note(4)
        self.cell_model.toggle_note(6)
        self.cell_model.clear()

        self.assertIsNone(self.cell_model.value)
        self.assertFalse(self.cell_model.in_conflict)
        self.assertEqual(self.cell_model.notes, [False for _ in range(BOARD_SIZE)])
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_clear_given(self):
        """ Ensures that clear cannot clear a given value"""
        self.cell_model.set_given(9)
        self.cell_model.clear()
        self.assertEqual(self.cell_model.value, 9)
        self.assertEqual(self.cell_model.value_type, CellValueType.GIVEN)

    def test_toggle_note_given(self):
        """ Ensures that toggling notes cannot clear given value"""
        self.cell_model.set_given(4)
        self.cell_model.toggle_note(3)
        self.assertEqual(self.cell_model.value, 4)
        self.assertEqual(self.cell_model.value_type, CellValueType.GIVEN)
        self.assertFalse(self.cell_model.notes[2])

    def test_is_entry(self):
        """ Makes sure is_entry is accurate. """
        self.cell_model.toggle_entry(1)
        self.assertTrue(self.cell_model.is_entry())

    def test_is_given(self):
        """ Makes sure is_given is accurate. """
        self.cell_model.set_given(1)
        self.assertTrue(self.cell_model.is_given())

    def test_is_notes(self):
        """ Makes sure is_notes is accurate. """
        self.cell_model.toggle_note(2)
        self.assertTrue(self.cell_model.is_notes())

    def test_is_blank(self):
        """ Tests that clearing resets to blank."""
        self.assertTrue(self.cell_model.is_blank())
        self.cell_model.toggle_entry(3)
        self.cell_model.clear()
        self.assertTrue(self.cell_model.is_blank())

        self.cell_model.toggle_note(3)
        self.cell_model.clear()
        self.assertTrue(self.cell_model.is_blank())

    def test_has_value(self):
        """ Tests that setting givens or entries is reflected in has_value() """
        self.assertFalse(self.cell_model.has_value())
        self.cell_model.toggle_entry(4)
        self.assertTrue(self.cell_model.has_value())

        self.cell_model.clear()
        self.assertFalse(self.cell_model.has_value())

        self.cell_model.set_given(5)
        self.assertTrue(self.cell_model.has_value())

    def test_has_note(self):
        """ Tests that toggling notes is reflected in has_note()"""
        self.assertFalse(self.cell_model.has_note(1))
        self.cell_model.toggle_note(1)
        self.assertTrue(self.cell_model.has_note(1))

    def test_note_cache(self):
        """ Tests that note cache is not cleared after toggling on an entry."""
        self.assertEqual(self.cell_model.notes, [False for _ in range(BOARD_SIZE)])
        self.cell_model.toggle_note(1)
        self.cell_model.toggle_entry(5)
        self.assertEqual(self.cell_model.notes, [True] + [False for _ in range(BOARD_SIZE - 1)])

    def test_set_conflict_status(self):
        """ Makes sure notify is called when setting status. """
        self.cell_model.notify = Mock()
        self.cell_model.set_conflict_status(True)
        self.assertTrue(self.cell_model.in_conflict)
        self.assertTrue(self.cell_model.notify.called)

        self.cell_model.set_conflict_status(False)
        self.assertFalse(self.cell_model.in_conflict)
        self.assertTrue(self.cell_model.notify.called)

    def test_get_house(self):
        self.cell_model.house_manager = Mock()
        self.cell_model.house_manager.get_house = Mock()
        self.cell_model.get_house()
        self.assertTrue(self.cell_model.house_manager.get_house.called)

    def test_get_row(self):
        self.cell_model.house_manager = Mock()
        self.cell_model.house_manager.get_row = Mock()
        self.cell_model.get_row()
        self.assertTrue(self.cell_model.house_manager.get_row.called)

    def test_get_column(self):
        self.cell_model.house_manager = Mock()
        self.cell_model.house_manager.get_column = Mock()
        self.cell_model.get_column()
        self.assertTrue(self.cell_model.house_manager.get_column.called)

    def test_get_subgrid(self):
        self.cell_model.house_manager = Mock()
        self.cell_model.house_manager.get_subgrid = Mock()
        self.cell_model.get_subgrid()
        self.assertTrue(self.cell_model.house_manager.get_subgrid.called)

    def test_get_possible_values(self):
        self.cell_model.value = None

        def _mock_get_house():
            """ Returns a list of mocked cells representing the house. """
            house = []
            # Create 8 mock cells with values and 1 mock cell (self.cell) without a value
            for i in range(8):
                mock_cell = Mock(spec=CellModel)
                mock_cell.value = i + 1 if i < 4 else None  # First 4 cells have values, next 4 cells are None
                house.append(mock_cell)
            return house

        self.cell_model.get_house = _mock_get_house

        # Check that the possible values are {5, 6, 7, 8, 9} since 1, 2, 3, 4 are used in the house
        possible_values = get_possible_values(self.cell_model)
        expected_values = {5, 6, 7, 8, 9}
        self.assertEqual(possible_values, expected_values)


if __name__ == '__main__':
    unittest.main()
