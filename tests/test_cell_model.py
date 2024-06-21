import unittest
from models.cell_model import CellModel
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
        self.cell_model.toggle_entry(1)
        self.assertTrue(self.cell_model.is_entry())

    def test_is_given(self):
        self.cell_model.set_given(1)
        self.assertTrue(self.cell_model.is_given())

    def test_is_notes(self):
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

