import unittest
from unittest.mock import Mock, patch
from tkinter import Tk

from utils.constants import BOARD_SIZE, SUBGRID_SIZE
from views.mode_button import ModeButton, Mode
from views.cell_view import CellView, CELL_SELECTION_COLOR, CELL_MATCHING_COLOR, CELL_HIGHLIGHT_COLOR
from controllers.board_controller import BoardController
from controllers.cell_controller import CellController
from models.cell_value_type import CellValueType
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
            [CellController(self.board_controller, self.board_view, self.board_model, x, y) for y in range(BOARD_SIZE)]
            for x in range(BOARD_SIZE)
        ]

    def tearDown(self):
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_initial_state(self):
        self.assertEqual(self.cell_controller.model.value, None)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.BLANK)
        self.assertFalse(self.cell_controller.model.in_conflict)
        self.assertListEqual(self.cell_controller.model.notes, [False] * BOARD_SIZE)

    def test_select(self):
        """ Ensures that select() properly selects and sets the color. """
        self.cell_controller.view.update_color = Mock()
        self.cell_controller.select()
        self.assertEqual(self.board_controller.selected_cell, self.cell_controller)
        self.cell_controller.view.update_color.assert_called_with(CELL_SELECTION_COLOR)

    def test_toggle_entry(self):
        """ Tests that setting the entry via toggle number works. """
        self.cell_controller.model.value = 1
        self.cell_controller.toggle_number(5)
        self.assertEqual(self.cell_controller.model.value, 5)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.ENTRY)
        self.cell_controller.view.update_labels.assert_called()

        self.cell_controller.toggle_number(5)
        self.assertEqual(self.cell_controller.model.value, None)
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.BLANK)
        self.cell_controller.view.update_labels.assert_called()

    def test_toggle_note(self):
        """ Tests that setting the note via toggle number works. """
        ModeButton.mode = Mode.NOTES
        self.cell_controller.toggle_number(5)
        self.assertTrue(self.cell_controller.model.notes[4])
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.NOTES)
        self.cell_controller.view.update_labels.assert_called()

        self.cell_controller.toggle_number(5)
        self.assertFalse(self.cell_controller.model.notes[4])
        self.assertEqual(self.cell_controller.model.value_type, CellValueType.BLANK)
        self.cell_controller.view.update_labels.assert_called()

    def test_toggle_given(self):
        self.cell_controller.model.value = 1
        self.cell_controller.model.value_type = CellValueType.GIVEN
        self.cell_controller.toggle_number(5)
        self.assertEqual(self.cell_controller.model.value, 1)

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
        another_cell_controller.view.update_color.assert_called_with(CELL_MATCHING_COLOR)

    def test_move_selection(self):
        """ Tests that this properly moves to another cell in the correct location. """
        self.cell_controller.move_selection(1, 0)
        self.assertEqual(self.board_controller.selected_cell, self.board_controller.cells[1][0])

    def test_get_row(self):
        row = self.cell_controller.get_row()
        expected_row = [self.board_controller.cells[0][i] for i in range(BOARD_SIZE) if i != 0]
        self.assert_matching_cells(row, expected_row)

    def test_get_column(self):
        column = self.cell_controller.get_column()
        expected_column = [self.board_controller.cells[i][0] for i in range(BOARD_SIZE) if i != 0]
        self.assert_matching_cells(column, expected_column)

    def test_get_subgrid(self):
        subgrid = self.cell_controller.get_subgrid()
        expected_subgrid = [
            self.cell_controllers[i][j]
            for i in range(0, SUBGRID_SIZE)
            for j in range(0, SUBGRID_SIZE)
            if (i, j) != (0, 0)
        ]
        self.assert_matching_cells(subgrid, expected_subgrid)

    def test_get_house(self):
        house = self.cell_controller.get_house()
        expected_house = [
            self.board_controller.cells[0][i] for i in range(BOARD_SIZE) if i != 0] + [
            self.board_controller.cells[i][0] for i in range(BOARD_SIZE) if i != 0] + [
            self.cell_controllers[i][j]
            for i in range(0, SUBGRID_SIZE)
            for j in range(0, SUBGRID_SIZE)
            if (i, j) != (0, 0)]
        self.assert_matching_cells(house, expected_house)

    def test_on_up(self):
        with patch.object(self.cell_controller.selection_manager, 'move_selection') as mock_move:
            self.cell_controller.event_handler.on_up(Mock())
            mock_move.assert_called_once_with(-1, 0)

    def test_on_down(self):
        with patch.object(self.cell_controller.selection_manager, 'move_selection') as mock_move:
            self.cell_controller.event_handler.on_down(Mock())
            mock_move.assert_called_once_with(1, 0)

    def test_on_left(self):
        with patch.object(self.cell_controller.selection_manager, 'move_selection') as mock_move:
            self.cell_controller.event_handler.on_left(Mock())
            mock_move.assert_called_once_with(0, -1)

    def test_on_right(self):
        with patch.object(self.cell_controller.selection_manager, 'move_selection') as mock_move:
            self.cell_controller.event_handler.on_right(Mock())
            mock_move.assert_called_once_with(0, 1)

    def test_on_key_press(self):
        with patch.object(self.cell_controller, 'toggle_number') as mock_toggle:
            event = Mock()
            event.keysym = '1'
            self.cell_controller.event_handler.on_key_press(event)
            mock_toggle.assert_called_once_with(1)

        event.keysym = 'a'
        self.cell_controller.event_handler.on_key_press(event)
        mock_toggle.assert_called_once()  # Ensure it was not called again

    def test_highlight_house(self):
        self.cell_controller.get_house()[0].view.update_color = Mock()
        self.cell_controller.highlight_house()
        self.cell_controller.get_house()[0].view.update_color.assert_called_with(CELL_HIGHLIGHT_COLOR)

    def test_pressed_notify(self):
        """ Ensures pressing on cell notifies observers of board model. """
        self.cell_controller.board_controller.model.notify = Mock()
        self.cell_controller.toggle_number(4)
        self.cell_controller.board_controller.model.notify.assert_called_once_with()

    def test_clear_notify(self):
        """ Ensures clear notifies observers of board model. """
        self.cell_controller.board_controller.model.notify = Mock()
        self.cell_controller.clear()
        self.cell_controller.board_controller.model.notify.assert_called_once_with()

    def test_valid_coordinates(self):
        with self.assertRaises(ValueError):
            cell = CellController(self.board_controller, Mock(), Mock(), 123, 12)

    def test_clearing_notes_in_house_on_entry(self):
        """ This tests that when the user makes an entry, all cells in the house get that note removed. """

        def setup_cell(_x, _y):
            self.board_controller.cells[_x][_y].toggle_number(5)
            self.board_controller.cells[_x][_y].toggle_number(4)

        ModeButton.mode = Mode.NOTES

        testing_cells = [(0, 4), (1, 4), (4, 0), (4, 1), (3, 3), (5, 5)]  # Includes same row, column and subgrid
        for x, y in testing_cells:
            setup_cell(x, y)

        ModeButton.mode = Mode.ENTRY
        self.board_controller.cells[4][4].toggle_number(5)

        # Makes sure 5 is cleared, but not 4
        for x, y in testing_cells:
            self.assertFalse(self.board_controller.cells[x][y].model.has_note(5), f"Note not cleared @ ({x}, {y})")
            self.assertTrue(self.board_controller.cells[x][y].model.has_note(4), f"Note cleared @ ({x}, {y})")

    def test_xy_set(self):
        self.cell_controller.model.x = 3
        self.cell_controller.model.y = 3

        self.cell_controller.x = 4
        self.cell_controller.y = 4

        self.assertEqual(self.cell_controller.model.x, 4)
        self.assertEqual(self.cell_controller.model.y, 4)

    def test_event_handler(self):
        self.cell_controller.clear = Mock()
        self.cell_controller.event_handler.clear()
        self.assertTrue(self.cell_controller.clear.called)

    #
    # Helper Methods
    #
    def assert_matching_cells(self, a, b):
        self.assertListEqual([(cell.model.x, cell.model.y) for cell in a],
                             [(cell.model.x, cell.model.y) for cell in b])


if __name__ == '__main__':
    unittest.main()
