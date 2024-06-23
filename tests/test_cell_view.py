import unittest
import random
from tkinter import Tk
from unittest.mock import Mock

from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from views.cell_view import *
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
        """ Test that the initial background color is set correctly."""
        self.assertEqual(self.cell_view['bg'], CellView._DEFAULT_COLOR)

    def test_update_labels_entry(self):
        """ Test that the entry value is displayed correctly and color is updated."""
        self.set_value(4, CellValueType.ENTRY)
        self.assertEqual(self.value_text, '4')
        self.assertEqual(self.value_fill, 'white')

    def test_update_labels_notes(self):
        """ Test that notes are displayed correctly and updated appropriately."""
        random.seed(42)  # Fix the seed for repeatability
        for _ in range(10):  # Test multiple scenarios
            notes_on = random.sample(range(BOARD_SIZE), k=random.randint(1, BOARD_SIZE))
            for i in range(BOARD_SIZE):
                self.model.notes[i] = i in notes_on

            self.model.value_type = CellValueType.NOTES
            self.cell_view.update_labels()

            for i in range(BOARD_SIZE):
                expected_text = str(i + 1) if i in notes_on else ''
                self.assertEqual(self.get_note_label(i), expected_text)

            notes_off = random.sample(notes_on, k=random.randint(0, len(notes_on)))
            for i in notes_off:
                self.model.notes[i] = False

            self.cell_view.update_labels()

            for i in range(BOARD_SIZE):
                expected_text = str(i + 1) if self.model.notes[i] else ''
                self.assertEqual(self.get_note_label(i), expected_text)

    def test_clear_entry(self):
        """ Test that clearing the entry label works correctly."""
        self.set_value(6, CellValueType.ENTRY)
        self.cell_view.clear_entry()
        self.assertEqual(self.cell_view.itemcget(self.cell_view.value_label, 'text'), '')

    def test_update_values_given(self):
        """ Test that given values are displayed correctly with the correct styling."""
        self.set_value(7, CellValueType.GIVEN)
        self.assertEqual(self.value_text, '7')
        self.assertEqual(self.value_fill, 'black')

    def test_given_stays_in_view(self):
        """ Test that clearing a given, or replacing with a note or entry has no effect in the view."""
        self.set_value(7, CellValueType.GIVEN)
        self.model.toggle_entry(3)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

        self.model.toggle_note(5)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

        self.model.clear_cell()
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '7')  # Value should remain 7

    def test_note_overriding(self):
        """ Tests that notes can override entries."""
        self.set_value(7, CellValueType.ENTRY)
        self.cell_view.update_labels()

        # Test that notes can hide entries
        self.model.toggle_entry(4)
        self.model.toggle_note(1)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '')

        # Test that entries will hide notes
        self.model.toggle_note(2)
        self.model.toggle_note(3)
        self.cell_view.update_labels()

        self.model.toggle_entry(2)
        self.cell_view.update_labels()

        for i in range(BOARD_SIZE):
            self.assertEqual(self.get_note_label(i), '')

        # Test that toggling entries off will restore notes
        self.model.toggle_entry(self.model.value)
        self.cell_view.update_labels()
        self.assertEqual(self.value_text, '')
        for i in range(SUBGRID_SIZE):
            self.assertEqual(self.get_note_label(i), str(i + 1))

        # Test that notes can be deleting when switching from entry back to notes
        self.model.toggle_entry(5)
        self.cell_view.update_labels()
        self.model.toggle_note(3)
        self.cell_view.update_labels()

        for i in range(2):
            self.assertEqual(self.get_note_label(i), str(i + 1))
        self.assertEqual(self.get_note_label(2), '')
        
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

    def get_note_label(self, index):
        return self.cell_view.itemcget(self.cell_view.note_labels[index], 'text')


class TestCellViewStateMachine(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        Initializes the Tkinter root, mock model, CellView, and StateContext.
        """
        self.root = Tk()
        self.model = Mock()
        self.model.in_conflict = False
        self.cell_view = CellView(self.root, self.model)
        self.state_context = self.cell_view._state_context

    def tearDown(self):
        """Clean up the Tkinter root after each test."""
        self.root.destroy()

    def test_enter_default(self):
        """Test entering the default state."""
        self.state_context.enter_default()
        self.assertIsInstance(self.state_context.state, DefaultCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#333')

    def test_enter_highlighted(self):
        """Test entering the highlighted state."""
        self.state_context.enter_highlighted()
        self.assertIsInstance(self.state_context.state, HighlightedCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#4a4a4a')

    def test_enter_selected(self):
        """Test entering the selected state."""
        self.state_context.enter_selected()
        self.assertIsInstance(self.state_context.state, SelectedCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), SELECTION_COLOR)

    def test_enter_matching(self):
        """Test entering the matching state."""
        self.state_context.enter_matching()
        self.assertIsInstance(self.state_context.state, MatchingCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#299')

    def test_enter_conflict(self):
        """Test entering the conflict state."""
        self.state_context.enter_conflict()
        self.assertIsInstance(self.state_context.state, ConflictCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#A33')

    def test_conflict_state_with_fallback(self):
        """
        Test entering and exiting the conflict state with a fallback state.
        Ensures the cell returns to the previous state after resolving the conflict.
        """
        self.state_context.enter_highlighted()
        self.state_context.enter_conflict()
        self.assertIsInstance(self.state_context.state, ConflictCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#A33')

        self.model.in_conflict = False
        self.state_context.exit_conflict()
        self.assertIsInstance(self.state_context.state, HighlightedCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#4a4a4a')

    def test_conflict_state_to_default(self):
        """
        Test entering and exiting the conflict state to the default state.
        Ensures the cell returns to the default state after resolving the conflict.
        """
        self.state_context.enter_default()
        self.state_context.enter_conflict()
        self.assertIsInstance(self.state_context.state, ConflictCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#A33')

        self.model.in_conflict = False
        self.state_context.exit_conflict()
        self.assertIsInstance(self.state_context.state, DefaultCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#333')

    def test_reset_state_from_conflict(self):
        """
        Test resetting the state from conflict to default.
        Ensures the cell returns to the default state after resetting.
        """
        self.state_context.enter_selected()
        self.state_context.enter_conflict()
        self.assertIsInstance(self.state_context.state, ConflictCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#A33')

        self.state_context.reset_state()
        self.assertIsInstance(self.state_context.state, DefaultCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#333')

    def test_reset_state_from_non_conflict(self):
        """
        Test resetting the state from a non-conflict state to default.
        Ensures the cell returns to the default state after resetting.
        """
        self.state_context.enter_selected()
        self.state_context.reset_state()
        self.assertIsInstance(self.state_context.state, DefaultCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#333')

    def test_try_set_state_conflict(self):
        """
        Test setting the state to conflict and then trying to set another state.
        Ensures the conflict state overrides other states.
        """
        self.state_context.enter_conflict()
        self.state_context.enter_highlighted()
        self.assertIsInstance(self.state_context.state, ConflictCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), '#A33')
        self.assertIsInstance(self.state_context.state.get_rollback_state(), HighlightedCellViewState)

    def test_exit_conflict_state_to_selected(self):
        """
        Test exiting the conflict state to the selected state.
        Ensures the cell returns to the selected state after resolving the conflict.
        """
        self.state_context.enter_selected()
        self.state_context.enter_conflict()
        self.model.in_conflict = False
        self.state_context.exit_conflict()
        self.assertIsInstance(self.state_context.state, SelectedCellViewState)
        self.assertEqual(self.cell_view.cget("bg"), SELECTION_COLOR)


if __name__ == '__main__':
    unittest.main()
