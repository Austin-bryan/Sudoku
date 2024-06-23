import unittest
from tkinter import Tk
from unittest.mock import Mock

from models.cell_value_type import CellValueType
from utils.constants import BOARD_SIZE
from views import number_button
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
        self.cell_controller.model.notes = [False] * BOARD_SIZE

        NumberButton.buttons = {i: NumberButton(self.root, self.board_controller, i) for i in range(1, BOARD_SIZE + 1)}

    def tearDown(self):
        self.root.destroy()
        NumberButton.buttons = {}
        NumberButton._selected_button = None

    def test_initial_state(self):
        self.assertFalse(NumberButton.buttons[1]._is_toggled)
        self.assertIn(1, NumberButton.buttons)

    def test_toggle_on(self):
        """ Tests that toggling on changes state and color. """
        NumberButton.buttons[1].toggle_on()
        self.assertTrue(NumberButton.buttons[1]._is_toggled)
        self.assertEqual(self.button1_fill, ToggleButton._TOGGLE_COLOR)

    def test_toggle_off(self):
        """ Tests that toggling off changes state and resets color. """
        NumberButton.buttons[1].toggle_on()
        NumberButton.buttons[1].toggle_off()
        self.assertFalse(NumberButton.buttons[1]._is_toggled)
        self.assertEqual(self.button1_fill, ToggleButton._DEFAULT_COLOR)

    def test_on_press(self):
        """ Tests that toggling on and off works. """
        self.cell_controller.model.is_given = Mock(return_value=False)
        NumberButton.buttons[1].enable()
        NumberButton.buttons[1].select(None)

        self.assertTrue(NumberButton.buttons[1]._is_toggled)
        self.board_controller.toggle_selected_cell.assert_called_with(1)

        NumberButton.buttons[1].select(None)
        self.assertFalse(NumberButton.buttons[1]._is_toggled)
        self.board_controller.toggle_selected_cell.assert_called_with(1)

    def test_entry_mode_turns_on_button(self):
        """ Tests that entering a number will show the correct entry button. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.is_given = Mock(return_value=False)
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        self.assertTrue(NumberButton.buttons[1]._is_toggled)

    def test_entry_mode_changes_button(self):
        """ Tests that entering a different entry will hide the previous entry button, and show the new one. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.is_given = Mock(return_value=False)
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        self.cell_controller.model.value = 2
        NumberButton.show_number_buttons(self.cell_controller)

        self.assertFalse(NumberButton.buttons[1]._is_toggled)
        self.assertTrue(NumberButton.buttons[2]._is_toggled)

    def test_notes_mode_turns_off_entry_button(self):
        """ Tests that changing to notes mode turns off the previously selected entry. """
        ModeButton.mode = Mode.ENTRY
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)
        self.assertFalse(NumberButton.buttons[1]._is_toggled)

    def test_notes_mode_turns_on_multiple_buttons(self):
        """ Tests that notes are capable of having multiple buttons on at once. """
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        self.cell_controller.model.value = None
        self.cell_controller.model.is_given = Mock(return_value=False)
        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(4):
            self.assertTrue(NumberButton.buttons[i + 1]._is_toggled)
        for i in range(5, BOARD_SIZE):
            self.assertFalse(NumberButton.buttons[i + 1]._is_toggled)

    def test_switching_back_to_entry_turns_off_note_buttons(self):
        ModeButton.mode = Mode.NOTES
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        NumberButton.show_number_buttons(self.cell_controller)
        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(BOARD_SIZE):
            self.assertFalse(NumberButton.buttons[i + 1]._is_toggled)

    def test_switching_back_to_notes_restores_cached_values(self):
        """ Tests that clicking back on the notes button will restore the cached note values. """
        ModeButton.mode = Mode.NOTES
        self.cell_controller.model.is_given = Mock(return_value=False)
        self.cell_controller.model.notes = [True] * 4 + [False] * 5
        NumberButton.show_number_buttons(self.cell_controller)

        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons(self.cell_controller)

        ModeButton.mode = Mode.NOTES
        NumberButton.show_number_buttons(self.cell_controller)

        for i in range(4):
            self.assertTrue(NumberButton.buttons[i + 1]._is_toggled)
        for i in range(5, BOARD_SIZE):
            self.assertFalse(NumberButton.buttons[i + 1]._is_toggled)

    def test_no_highlight_givens(self):
        """ Makes sure tha givens highlight number buttons, as they can't be changed"""
        self.assertFalse(NumberButton.buttons[1]._is_toggled)

        self.cell_controller.model.value = 1
        self.cell_controller.model.value_type = CellValueType.GIVEN
        NumberButton.show_number_buttons(self.cell_controller)

        self.assertFalse(NumberButton.buttons[1]._is_toggled)

    def test_all_buttons_disabled_at_start(self):
        """ Tests that all number buttons are disabled at start. """
        for button in NumberButton.buttons.values():
            self.assertTrue(button._is_disabled)

    def test_selecting_any_cell_enables_all_buttons(self):
        """ Tests that selecting any cell enables all buttons. """
        self.cell_controller.model.is_given = Mock(return_value=False)
        self.cell_controller.model.value = 1
        NumberButton.show_number_buttons(self.cell_controller)
        for button in NumberButton.buttons.values():
            self.assertFalse(button._is_disabled)

    def test_selecting_given_disables_all_buttons(self):
        """ Tests that selecting a given disables all buttons. """
        self.cell_controller.model.is_given = Mock(return_value=True)
        NumberButton.show_number_buttons(self.cell_controller)
        for button in NumberButton.buttons.values():
            self.assertTrue(button._is_disabled)

    def test_disabled_buttons_cannot_hover(self):
        """ Tests that disabled buttons do not change color on hover. """
        button = NumberButton.buttons[1]
        button.disable()
        button.on_enter(None)
        self.assertEqual(self.button1_fill, NumberButton._DISABLED_FILL)

    def test_disabled_buttons_cannot_click(self):
        """ Tests that disabled buttons do not change state or color on click. """
        button = NumberButton.buttons[1]
        button.disable()
        button.select(None)
        self.assertFalse(button._is_toggled)
        self.assertEqual(self.button1_fill, NumberButton._DISABLED_FILL)

    def test_disabled_buttons_cannot_leave(self):
        """ Tests that disabled buttons do not change color on leave. """
        button = NumberButton.buttons[1]
        button.disable()
        button.on_leave(None)
        self.assertEqual(self.button1_fill, NumberButton._DISABLED_FILL)

    def test_enabled_enter(self):
        """ Makes sure that enabled buttons can have hover effect. """
        button = NumberButton.buttons[1]
        button.enable()
        button.on_enter(None)
        self.assertEqual(self.button1_fill, NumberButton._HOVER_COLOR)

    def test_enabled_leave(self):
        """ Makes sure that enabled buttons can remove hover effect. """
        button = NumberButton.buttons[1]
        button.enable()
        button.on_enter(None)
        button.on_leave(None)
        self.assertEqual(self.button1_fill, NumberButton._DEFAULT_COLOR)


    def test_pressing_changes_color(self):
        """ Makes sure clicking on the button will change the color. """
        NumberButton.buttons[1].enable()
        button = NumberButton.buttons[1]
        button.select(None)
        self.assertEqual(self.button1_fill, NumberButton._TOGGLE_COLOR)

        button.select(None)
        self.assertEqual(self.button1_fill, NumberButton._DEFAULT_COLOR)

    def test_pressing_multiple_notes(self):
        """ Tests that multiple notes can be on at once. """
        NumberButton.buttons[1].enable()
        NumberButton.buttons[2].enable()
        ModeButton.mode = Mode.NOTES
        NumberButton.buttons[1].select(None)
        NumberButton.buttons[2].select(None)

        self.assertEqual(self.button1_fill, NumberButton._TOGGLE_COLOR)
        self.assertEqual(self.button2_fill, NumberButton._TOGGLE_COLOR)

    def test_pressing_multiple_entries(self):
        """ Tests that multiple entries will turn the active one off. """
        NumberButton.buttons[1].enable()
        NumberButton.buttons[2].enable()
        ModeButton.mode = Mode.ENTRY
        NumberButton.buttons[1].select(None)
        NumberButton.buttons[2].select(None)

        self.assertEqual(self.button1_fill, NumberButton._DEFAULT_COLOR)
        self.assertEqual(self.button2_fill, NumberButton._TOGGLE_COLOR)

    @property
    def button1_fill(self):
        return NumberButton.buttons[1].itemcget(NumberButton.buttons[1].rect, 'fill')

    @property
    def button2_fill(self):
        return NumberButton.buttons[2].itemcget(NumberButton.buttons[1].rect, 'fill')


if __name__ == '__main__':
    unittest.main()
