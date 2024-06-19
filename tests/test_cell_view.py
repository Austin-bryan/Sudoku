import unittest
import random
from tkinter import Tk
from views.cell_view import CellView
from models.cell_model import CellModel
from models.cell_value_type import CellValueType


class TestCellView(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.model = CellModel(0, 0)
        self.cell_view = CellView(self.root, self.model)

    def tearDown(self):
        self.root.destroy()

    def test_initial_color(self):
        """Test that the initial background color is set correctly."""
        self.assertEqual(self.cell_view['bg'], CellView._DEFAULT_COLOR)

    def test_update_labels_entry(self):
        """Test that the entry value is displayed correctly and color is updated."""
        self.set_value(4, CellValueType.ENTRY)
        self.assertEqual(self.value_text, '4')
        self.assertEqual(self.value_fill, 'white')

    def test_update_labels_notes(self):
        """Test that notes are displayed correctly and updated appropriately."""
        random.seed(42)  # Fix the seed for repeatability
        for _ in range(10):  # Test multiple scenarios
            notes_on = random.sample(range(9), k=random.randint(1, 9))
            for i in range(9):
                self.model.notes[i] = i in notes_on

            self.model.value_type = CellValueType.NOTES
            self.cell_view.update_labels()

            for i in range(9):
                expected_text = str(i + 1) if i in notes_on else ''
                self.assertEqual(self.cell_view.itemcget(self.cell_view.note_labels[i], 'text'), expected_text)

            notes_off = random.sample(notes_on, k=random.randint(0, len(notes_on)))
            for i in notes_off:
                self.model.notes[i] = False

            self.cell_view.update_labels()

            for i in range(9):
                expected_text = str(i + 1) if self.model.notes[i] else ''
                self.assertEqual(self.cell_view.itemcget(self.cell_view.note_labels[i], 'text'), expected_text)

    def test_clear_entry(self):
        """Test that clearing the entry label works correctly."""
        self.set_value(6, CellValueType.ENTRY)
        self.cell_view.clear_entry()
        self.assertEqual(self.cell_view.itemcget(self.cell_view.value_label, 'text'), '')

    def test_update_values_given(self):
        """Test that given values are displayed correctly with the correct styling."""
        self.set_value(7, CellValueType.GIVEN)
        self.assertEqual(self.value_text, '7')
        self.assertEqual(self.value_fill, 'black')

    def test_given_stays_in_view(self):
        """Test that clearing a given, or replacing with a note or entry has no effect in the view."""
        self.set_value(7, CellValueType.GIVEN)
        self.model.toggle_entry(3)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

        self.model.toggle_note(5)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

        self.model.clear()
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

    #
    # Helper Methods
    #
    def set_value(self, value, value_type):
        """Helper method to set the model value and update the cell view labels."""
        self.model.value = value
        self.model.value_type = value_type
        self.cell_view.update_labels()

    @property
    def value_text(self):
        return self.cell_view.itemcget(self.cell_view.value_label, 'text')

    @property
    def value_fill(self):
        return self.cell_view.itemcget(self.cell_view.value_label, 'fill')


if __name__ == '__main__':
    unittest.main()
