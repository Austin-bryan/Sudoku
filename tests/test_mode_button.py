import unittest
from tkinter import Tk
from views.mode_button import ModeButton, Mode
from unittest.mock import patch, Mock
from views.number_button import NumberButton


class TestModeButton(unittest.TestCase):
    @patch('views.action_button.ActionButton.create_icon')
    def setUp(self, mock_create_icon):
        mock_create_icon.return_value = (Mock(), Mock())
        self.root = Tk()
        self.root.withdraw()
        self.mode_button = ModeButton(self.root, Mock(), 'Notes')
        self.mode_button = ModeButton(self.root, Mock(), 'Notes')
        self.show_number_buttons = NumberButton.show_number_buttons
        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        from time import sleep
        self.root.update_idletasks()
        # sleep(0.1)
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    @patch('views.action_button.ActionButton.create_icon')
    def test_initial_mode(self, mock_create_icon):
        """ Test that the initial mode is ENTRY. """
        self.assertEqual(ModeButton.mode, Mode.ENTRY)

    @patch('views.action_button.ActionButton.create_icon')
    def test_mode_switching(self, mock_create_icon):
        """ Test that mode switches between ENTRY and NOTES. """
        self.mode_button.on_press(None)
        self.assertEqual(ModeButton.mode, Mode.NOTES)
        self.mode_button.on_press(None)
        self.assertEqual(ModeButton.mode, Mode.ENTRY)

    @patch('views.number_button.NumberButton.show_number_buttons')
    @patch('views.action_button.ActionButton.create_icon')
    def test_show_number_buttons_called_on_press(self, mock_create_icon, mock_show_number_buttons):
        """ Test that show_number_buttons is called when the button is pressed. """
        self.mode_button.on_press(None)
        mock_show_number_buttons.assert_called()


if __name__ == '__main__':
    unittest.main()
