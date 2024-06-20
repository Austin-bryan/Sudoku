import unittest
from tkinter import Tk
from unittest.mock import Mock

from models.cell_value_type import CellValueType
from views.mode_button import ModeButton, Mode
from views.number_button import NumberButton
from controllers.board_controller import BoardController
from views.toggle_button import ToggleButton


class TestNumberButton(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.board_controller = Mock(BoardController)
        self.cell_controller = Mock()
        self.cell_controller.model.value = None
        self.cell_controller.model.notes = [False] * 9

        NumberButton.buttons = {i: NumberButton(self.root, self.board_controller, i) for i in range(1, 10)}

    def tearDown(self):
        self.root.destroy()
        NumberButton.buttons = {}
        NumberButton.__selected_button = None

    def test_initial_state(self):
        self.assertFalse(NumberButton.buttons[1].is_toggled)
        self.assertIn(1, NumberButton.buttons)

    def test_toggle_on(self):
        """ Tests that toggling on changes state and color. """
        NumberButton.buttons[1].toggle_on()
        self.assertTrue(NumberButton.buttons[1].is_toggled)
        self.assertEqual(self.button_fill, ToggleButton._TOGGLE_COLOR)

    def test_toggle_off(self):
        """ Tests that toggling off changes state and resets color. """
        NumberButton.buttons[1].toggle_on()
        NumberButton.buttons[1].toggle_off()
        self.assertFalse(NumberButton.buttons[1].is_toggled)
        self.assertEqual(self.button_fill, ToggleButton._DEFAULT_COLOR)

    def test_on_press(self):
        """ Tests that toggling on and off works. """
        NumberButton.buttons[1].on_press(None)
        self.assertTrue(NumberButton.buttons[1].is_toggled)
        self.board_controller.toggle_selected_cell.assert_called_with(1)

        NumberButton.buttons[1].on_press(None)
        self.assertFalse(NumberButton.buttons[1].is_toggled)
        self.board_controller.toggle_selected_cell.assert_called_with(1)

    def test_entry_mode_turns_on_button(self):
        """ Tests that entering a number will show the correct entry button. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        self.assertTrue(NumberButton.buttons[1].is_toggled)

    def test_entry_mode_changes_button(self):
        """ Tests that entering a different entry will hide the previous entry button, and show the new one. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        self.cell_controller.model.value = 2
        NumberButton.show_number_buttons(self.cell_controller)

        self.assertFalse(NumberButton.buttons[1].is_toggled)
        self.assertTrue(NumberButton.buttons[2].is_toggled)

    def test_notes_mode_turns_off_entry_button(self):
        """ Tests that changing to notes mode turns off the previously selected entry. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)
        self.assertFalse(NumberButton.buttons[1].is_toggled)

    def test_notes_mode_turns_on_multiple_buttons(self):
        """ Tests that notes are capable of having multiple buttons on at once. """
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        self.cell_controller.model.value = None
        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(4):
            self.assertTrue(NumberButton.buttons[i + 1].is_toggled)
        for i in range(5, 9):
            self.assertFalse(NumberButton.buttons[i + 1].is_toggled)

    def test_switching_back_to_entry_turns_off_note_buttons(self):
        ModeButton.mode = Mode.NOTES
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        NumberButton.show_number_buttons(self.cell_controller)
        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(9):
            self.assertFalse(NumberButton.buttons[i + 1].is_toggled)

    def test_switching_back_to_notes_restores_cached_values(self):
        """ Tests that clicking back on the notes button will restore the cached note values. """
        ModeButton.mode = Mode.NOTES
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        NumberButton.show_number_buttons(self.cell_controller)

        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons(self.cell_controller)

        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(4):
            self.assertTrue(NumberButton.buttons[i + 1].is_toggled)
        for i in range(5, 9):
            self.assertFalse(NumberButton.buttons[i + 1].is_toggled)

    def test_no_highlight_givens(self):
        self.assertFalse(NumberButton.buttons[1].is_toggled)

        self.cell_controller.model.value = 1
        self.cell_controller.model.value_type = CellValueType.GIVEN
        NumberButton.show_number_buttons(self.cell_controller)

        self.assertFalse(NumberButton.buttons[1].is_toggled)

    @property
    def button_fill(self):
        return NumberButton.buttons[1].itemcget(NumberButton.buttons[1].rect, 'fill')


if __name__ == '__main__':
    unittest.main()
