import unittest
from unittest.mock import Mock, patch
from tkinter import Tk

from mode_button import ModeButton, Mode
from models.cell_model import CellModel
from views.cell_view import CellView
from controllers.cell_controller import CellController
from models.cell_value_type import CellValueType
from controllers.board_controller import BoardController
from views.board_view import BoardView
from models.board_model import BoardModel
from number_button import NumberButton


class TestCellController(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.board_model = BoardModel()
        self.board_view = BoardView(self.root)
        self.board_controller = BoardController(self.root)
        self.cell_controller = CellController(self.board_controller, self.board_view, self.board_model, 0, 0)
        self.cell_controller.view.update_labels = Mock()
        NumberButton.show_number_buttons = Mock()

        self.cell_controllers = [
            [CellController(self.board_controller, self.board_view, self.board_model, x, y) for y in range(9)]
            for x in range(9)
        ]

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.cell_controller.model.value, None)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.BLANK)
        self.assertFalse(self.cell_controller.model.in_conflict)
        self.assertListEqual(self.cell_controller.model.notes, [False] * 9)

    def test_on_press(self):
        """ Ensures that on_press() properly selects and sets the color. """
        self.cell_controller.view.update_color = Mock()
        self.cell_controller.on_press(None)
        self.assertEqual(self.board_controller.selected_cell, self.cell_controller)
        self.cell_controller.view.update_color.assert_called_with(CellView._PRESS_COLOR)

    def test_toggle_entry(self):
        """ Tests that setting the entry via toggle number works. """
        self.cell_controller.toggle_number(5)
        self.assertEqual(self.cell_controller.model.value, 5)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.ENTRY)
        self.cell_controller.view.update_labels.assert_called()

    def test_toggle_note(self):
        """ Tests that setting the note via toggle number works. """
        ModeButton.mode = Mode.NOTES
        self.cell_controller.toggle_number(5)
        self.assertTrue(self.cell_controller.model.notes[4])
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.NOTES)
        self.cell_controller.view.update_labels.assert_called()

    def test_clear(self):
        """ Tests that clear works. """
        self.cell_controller.model.value = 5
        self.cell_controller.model.value_type = CellValueType.ENTRY
        self.cell_controller.clear()
        self.assertEqual(self.cell_controller.model.value, None)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.BLANK)
        self.cell_controller.view.update_labels.assert_called()

    def test_highlight_matching_numbers(self):
        """ Ensures that highlighting of matching colors works properly. """
        self.cell_controller.model.value = 5
        self.cell_controller.highlight_matching_numbers()
        # Assuming there's another cell with the same value
        another_cell_controller = self.board_controller.cells[1][1]
        another_cell_controller.model.value = 5

        another_cell_controller.view.update_color = Mock()
        self.cell_controller.highlight_matching_numbers()
        another_cell_controller.view.update_color.assert_called_with(CellView._MATCHING_COLOR)

    def test_move_selection(self):
        """ Tests that this properly moves to another cell in the correct location. """
        self.cell_controller.move_selection(1, 0)
        self.assertEqual(self.board_controller.selected_cell, self.board_controller.cells[1][0])

    def test_get_row(self):
        row = self.cell_controller.get_row()
        expected_row = [self.board_controller.cells[0][i] for i in range(9) if i != 0]
        self.assertListEqual([(cell.model.x, cell.model.y) for cell in row], [(cell.model.x, cell.model.y) for cell in expected_row])

    def test_get_column(self):
        column = self.cell_controller.get_column()
        expected_column = [self.board_controller.cells[i][0] for i in range(9) if i != 0]
        self.assertListEqual([(cell.model.x, cell.model.y) for cell in column],
                             [(cell.model.x, cell.model.y) for cell in expected_column])

    def test_get_square(self):
        square = self.cell_controller.get_square()
        expected_square = [
            self.cell_controllers[i][j]
            for i in range(0, 3)
            for j in range(0, 3)
            if (i, j) != (0, 0)
        ]
        self.assertListEqual([(cell.model.x, cell.model.y) for cell in square],
                             [(cell.model.x, cell.model.y) for cell in expected_square])


if __name__ == '__main__':
    unittest.main()
