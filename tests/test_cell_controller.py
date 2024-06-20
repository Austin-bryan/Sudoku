import unittest
from unittest.mock import Mock, patch
from tkinter import Tk

from views.mode_button import ModeButton, Mode
from views.cell_view import CellView
from controllers.cell_controller import CellController
from models.cell_value_type import CellValueType
from controllers.board_controller import BoardController
from views.board_view import BoardView
from models.board_model import BoardModel
from views.number_button import NumberButton


class TestCellController(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.board_model = BoardModel()
        self.board_view = BoardView(self.root)
        self.board_controller = BoardController(self.root)
        self.cell_controller = CellController(self.board_controller, self.board_view, self.board_model, 0, 0)
        self.cell_controller.view.update_labels = Mock()
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

        self.cell_controllers = [
            [CellController(self.board_controller, self.board_view, self.board_model, x, y) for y in range(9)]
            for x in range(9)
        ]

    def tearDown(self):
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

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
        self.assert_matching_cells(row, expected_row)

    def test_get_column(self):
        column = self.cell_controller.get_column()
        expected_column = [self.board_controller.cells[i][0] for i in range(9) if i != 0]
        self.assert_matching_cells(column, expected_column)

    def test_get_square(self):
        square = self.cell_controller.get_square()
        expected_square = [
            self.cell_controllers[i][j]
            for i in range(0, 3)
            for j in range(0, 3)
            if (i, j) != (0, 0)
        ]
        self.assert_matching_cells(square, expected_square)

    def test_get_house(self):
        house = self.cell_controller.get_house()
        expected_house = [
            self.board_controller.cells[0][i] for i in range(9) if i != 0] + [
            self.board_controller.cells[i][0] for i in range(9) if i != 0] + [
            self.cell_controllers[i][j]
            for i in range(0, 3)
            for j in range(0, 3)
            if (i, j) != (0, 0)]
        self.assert_matching_cells(house, expected_house)

    def test_on_up(self):
        with patch.object(self.cell_controller, 'move_selection') as mock_move:
            self.cell_controller.on_up(Mock())
            mock_move.assert_called_once_with(-1, 0)

    def test_on_down(self):
        with patch.object(self.cell_controller, 'move_selection') as mock_move:
            self.cell_controller.on_down(Mock())
            mock_move.assert_called_once_with(1, 0)

    def test_on_left(self):
        with patch.object(self.cell_controller, 'move_selection') as mock_move:
            self.cell_controller.on_left(Mock())
            mock_move.assert_called_once_with(0, -1)

    def test_on_right(self):
        with patch.object(self.cell_controller, 'move_selection') as mock_move:
            self.cell_controller.on_right(Mock())
            mock_move.assert_called_once_with(0, 1)

    def test_on_key_press(self):
        with patch.object(self.cell_controller, 'toggle_number') as mock_toggle:
            event = Mock()
            event.keysym = '1'
            self.cell_controller.on_key_press(event)
            mock_toggle.assert_called_once_with(1)

        event.keysym = 'a'
        self.cell_controller.on_key_press(event)
        mock_toggle.assert_called_once()  # Ensure it was not called again

    def test_highlight_house(self):
        self.cell_controller.get_house()[0].view.update_color = Mock()
        self.cell_controller.highlight_house()
        self.cell_controller.get_house()[0].view.update_color.assert_called_with(CellView._HIGHLIGHT_COLOR)

    #
    # Helper Methods
    #
    def assert_matching_cells(self, a, b):
        self.assertListEqual([(cell.model.x, cell.model.y) for cell in a],
                             [(cell.model.x, cell.model.y) for cell in b])


if __name__ == '__main__':
    unittest.main()
