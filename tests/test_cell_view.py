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
        self.assertEqual(self.cell_view['bg'], CellView._DEFAULT_COLOR)

    def test_update_labels_entry(self):
        self.set_entry(4)
        self.assertEqual(self.cell_view.itemcget(self.cell_view.entry_label, 'text'), 5)

    def test_update_labels_notes(self):
        random.seed(42)  # Fix the seed for repeatability
        for _ in range(10):  # Test multiple scenarios
            # Randomly set notes
            notes_on = random.sample(range(9), k=random.randint(1, 9))
            for i in range(9):
                self.model.notes[i] = i in notes_on

            self.model.value_type = CellValueType.NOTES
            self.cell_view.update_labels()

            # Check that the notes are correctly displayed
            for i in range(9):
                expected_text = str(i + 1) if i in notes_on else ''
                self.assertEqual(self.cell_view.itemcget(self.cell_view.note_labels[i], 'text'), expected_text)

            # Randomly turn off some notes
            notes_off = random.sample(notes_on, k=random.randint(0, len(notes_on)))
            for i in notes_off:
                self.model.notes[i] = False

            self.cell_view.update_labels()

            # Check that the notes are correctly displayed after turning off
            for i in range(9):
                expected_text = str(i + 1) if self.model.notes[i] else ''
                self.assertEqual(self.cell_view.itemcget(self.cell_view.note_labels[i], 'text'), expected_text)

    def test_clear_entry(self):
        self.set_entry(6)
        self.cell_view.clear_entry()
        self.assertEqual(self.cell_view.itemcget(self.cell_view.entry_label, 'text'), '')

    def set_entry(self, value):
        self.model.value = value
        self.model.value_type = CellValueType.ENTRY
        self.cell_view.update_labels()
