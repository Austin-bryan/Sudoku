import unittest
from unittest.mock import Mock
from tkinter import Tk

from views.action_button import ActionButton, BUTTON_HOVER_COLOR, \
    BUTTON_DEFAULT_COLOR  # Replace with the actual import path


class TestActionButton(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()  # Hide the main window

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        button = ActionButton(self.root, 'Test', font_size=12, width=100, height=50, bg='#123456')
        self.assertEqual(button.label, 'Test')
        self.assertEqual(button.bg, '#123456')
        self.assertEqual(button['width'], '100')
        self.assertEqual(button['height'], '50')

    def test_hover_effect(self):
        button = ActionButton(self.root, 'Test')
        button.on_enter(None)
        self.assertEqual(button.itemcget(button.rect, 'fill'), BUTTON_HOVER_COLOR)
        button.on_leave(None)
        self.assertEqual(button.itemcget(button.rect, 'fill'), BUTTON_DEFAULT_COLOR)

    def test_custom_background_color(self):
        button = ActionButton(self.root, 'Test', bg='#123456')
        button.on_leave(None)
        self.assertEqual(button.itemcget(button.rect, 'fill'), '#123456')

    def test_command_execution(self):
        mock_command = Mock()
        button = ActionButton(self.root, 'Test', command=mock_command)
        button.on_press(None)
        button.command.assert_called_once()

    def test_icon_creation(self):
        button = ActionButton(self.root, 'Test', image_path='clear.png')
        self.assertIsNotNone(button.photo_image)
        self.assertIsNotNone(button.image_item)


if __name__ == '__main__':
    unittest.main()
