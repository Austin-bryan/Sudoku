import unittest
from tkinter import Tk
from views.mode_button import ModeButton, Mode
from unittest.mock import patch, Mock
from views.number_button import NumberButton


class TestModeButton(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.mode_button = ModeButton(self.root, Mock(), 'M')
        self.show_number_buttons = NumberButton.show_number_buttons
        ModeButton.mode = Mode.ENTRY
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_initial_mode(self):
        """ Test that the initial mode is ENTRY. """
        self.assertEqual(ModeButton.mode, Mode.ENTRY)

    def test_mode_switching(self):
        """ Test that mode switches between ENTRY and NOTES. """
        self.mode_button.on_press(None)
        self.assertEqual(ModeButton.mode, Mode.NOTES)
        self.mode_button.on_press(None)
        self.assertEqual(ModeButton.mode, Mode.ENTRY)

    @patch('views.number_button.NumberButton.show_number_buttons')
    def test_show_number_buttons_called_on_press(self, mock_show_number_buttons):
        """ Test that show_number_buttons is called when the button is pressed. """
        self.mode_button.on_press(None)
        mock_show_number_buttons.assert_called()


if __name__ == '__main__':
    unittest.main()
