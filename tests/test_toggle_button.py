# tests/test_toggle_button.py

import unittest
from tkinter import Tk
from unittest.mock import Mock

from views.toggle_button import ToggleButton


class TestToggleButton(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.toggle_button = ToggleButton(self.root, 'Test')

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertFalse(self.toggle_button._is_toggled)
        self.assertEqual(self.button_fill, ToggleButton._DEFAULT_COLOR)

    def test_toggle_on(self):
        """ Asserts state changes correctly and updates color. """
        self.toggle_button.toggle_on()
        self.assertTrue(self.toggle_button._is_toggled)
        self.assertEqual(self.button_fill, ToggleButton._TOGGLE_COLOR)

    def test_toggle_off(self):
        """ Asserts state changes correctly and updates color. """
        self.toggle_button.toggle_on()
        self.toggle_button.toggle_off()
        self.assertFalse(self.toggle_button._is_toggled)
        self.assertEqual(self.button_fill, ToggleButton._DEFAULT_COLOR)

    def test_enter(self):
        """ Tests that hovering works. """
        self.toggle_button.on_enter(Mock())
        self.assertTrue(self.button_fill, ToggleButton._HOVER_COLOR)

    def test_leave(self):
        """ Tests that leaving restores to default color. """
        self.toggle_button.on_leave(Mock())
        self.assertTrue(self.button_fill, ToggleButton._DEFAULT_COLOR)

    def test_toggled_on_enter(self):
        """ Tests that hovering has no effect if toggled on. """
        self.toggle_button.toggle_on()
        self.toggle_button.on_enter(Mock())
        self.assertTrue(self.button_fill, ToggleButton._TOGGLE_COLOR)

    def test_toggled_on_leave(self):
        """ Tests that leaving has no effect if toggled on. """
        self.toggle_button.toggle_on()
        self.toggle_button.on_enter(Mock())
        self.toggle_button.on_leave(Mock())
        self.assertTrue(self.button_fill, ToggleButton._TOGGLE_COLOR)

    def test_on_press_toggle(self):
        self.toggle_button.on_press(None)
        self.assertTrue(self.toggle_button._is_toggled)
        self.toggle_button.on_press(None)
        self.assertFalse(self.toggle_button._is_toggled)

    @property
    def button_fill(self):
        return self.toggle_button.itemcget(self.toggle_button.rect, 'fill')

if __name__ == '__main__':
    unittest.main()
