import time
import unittest
from tkinter import Tk
from unittest.mock import MagicMock, Mock, patch

from controllers.board_controller import BoardController
from controllers.cell_controller import CellController
from models.cell_model import CellModel
from models.cell_value_type import CellValueType
from observers.conflict_observer import ConflictObserver
from undo_history.cell_commands import *
from utils.backtracking_solver import BacktrackingSolver
from utils.sudoku_generator import SudokuGenerator
from views.board_view import BoardView
from views.number_button import NumberButton


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.cell_model = CellModel(0, 0)
        self.cell_controller = MagicMock()
        self.cell_controller.model = self.cell_model
        self.board_model = MagicMock()
        self.cell_controller.board_controller.model = self.board_model
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

    def tearDown(self):
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_set_entry_on_empty_cell(self):
        """ Tests that starting from a blank cell, entering a value, undoing will restore to blank. """
        self.cell_model.value = None
        self.cell_model.notes = [False] * 9
        self.cell_model.value_type = CellValueType.BLANK

        command = ToggleEntryCommand(self.cell_controller, 5)
        command.execute()
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

        command.undo()
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_delete_entry_and_restore(self):
        """ Tests that starting with a full cell and deleting will restore it to its original value. """
        self.cell_model.value = 5
        self.cell_model.notes = [False] * 9
        self.cell_model.value_type = CellValueType.ENTRY

        command = ClearCellCommand(self.cell_controller)
        command.execute()
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

        command.undo()
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

    def test_add_note_to_blank_cell(self):
        """ Asserts that adding a note will turn it on, but undoing will revert until its a blank cell again. """
        self.cell_model.value = None
        self.cell_model.notes = [False] * 9
        self.cell_model.value_type = CellValueType.BLANK

        command1 = ToggleNoteCommand(self.cell_controller, 3)
        command1.execute()
        self.assertTrue(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

        command2 = ToggleNoteCommand(self.cell_controller, 5)
        command2.execute()
        self.assertTrue(self.cell_model.notes[4])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

        command2.undo()
        self.assertFalse(self.cell_model.notes[4])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

        command1.undo()
        self.assertFalse(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

    def test_toggle_off_note(self):
        """ Asserts that toggling off a note can be undone, restoring the note. """
        self.cell_model.value = None
        self.cell_model.notes = [False] * 9
        self.cell_model.notes[2] = True
        self.cell_model.value_type = CellValueType.NOTES

        command = ToggleNoteCommand(self.cell_controller, 3)
        command.execute()
        self.assertFalse(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

        command.undo()
        self.assertTrue(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

    def test_toggle_entry_and_add_note_then_undo(self):
        """
        Asserts that, if starting from an entry then toggling a note, it will switch to a note,
        and that this operation can be undone, restore the entry.
        """
        self.cell_model.value = 5
        self.cell_model.notes = [False] * 9
        self.cell_model.value_type = CellValueType.ENTRY

        note_command = ToggleNoteCommand(self.cell_controller, 3)
        note_command.execute()
        self.assertTrue(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

        note_command.undo()
        self.assertFalse(self.cell_model.notes[2])
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

    def test_clear_notes_and_restore(self):
        """ Asserts that when clearing notes, all notes can be restored via undo operation. """
        self.cell_model.value = None
        self.cell_model.notes = [True] * 3 + [False] * 6
        self.cell_model.value_type = CellValueType.NOTES

        command = ClearCellCommand(self.cell_controller)
        command.execute()
        self.assertIsNone(self.cell_model.value)
        self.assertFalse(any(self.cell_model.notes))
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

        command.undo()
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.notes, [True] * 3 + [False] * 6)
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

    def test_replace_notes_with_entry_and_restore_notes(self):
        """ Asserts that replacing notes with an entry can be undone, restoring the notes. """
        self.cell_model.value = None
        self.cell_model.notes = [True] * 3 + [False] * 6
        self.cell_model.value_type = CellValueType.NOTES

        command = ToggleEntryCommand(self.cell_controller, 5)
        command.execute()
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)
        self.assertEqual(self.cell_model.notes, [True] * 3 + [False] * 6)

        command.undo()
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.notes, [True] * 3 + [False] * 6)
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)

    def test_clear_note_from_house_on_entry_and_restore(self):
        """
        When an entry is made, it clears all notes in the same house of the same value.
        This asserts that undoing an entry operation will restore the notes it cleared.
        """
        self.cell_model.value = None
        self.cell_model.notes = [False] * 9
        self.cell_model.value_type = CellValueType.BLANK

        # Setup board controller with required items
        root = Tk()
        root.withdraw()
        board_view = BoardView(root)
        board_controller = BoardController(root, Mock())

        # Populate the house with test notes of 2, 3
        house_cells = [CellController(board_controller, board_view, Mock(), 0, 0) for _ in range(8)]
        for cell in house_cells:
            cell.model.notes = [False, True, True] + [False] * 6
            cell.model.value = None
            cell.model.value_type = CellValueType.NOTES

        self.cell_controller.get_house.return_value = house_cells

        # Toggle on the number 3, which should clear it from the notes
        command = ToggleEntryCommand(self.cell_controller, 3)
        command.execute()
        self.assertEqual(self.cell_model.value, 3)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

        # Test that the 3 note is cleared from all notes in house, but 1 is untouched.
        for cell in house_cells:
            self.assertFalse(cell.model.notes[2])

        for cell in house_cells:
            self.assertTrue(cell.model.notes[1])

        command.undo()
        self.assertIsNone(self.cell_model.value)
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)

        # Make sure both notes are active, with 3 just now being restored
        for cell in house_cells:
            self.assertTrue(cell.model.notes[2])

        for cell in house_cells:
            self.assertTrue(cell.model.notes[1])

        root.destroy()

    def test_restore_notes_after_entry_and_clear(self):
        """ Ensures that after setting notes, setting an entry, then clearing, the notes state can be restored."""
        self.cell_model.value = None
        self.cell_model.notes = [True] * 3 + [False] * 6
        self.cell_model.value_type = CellValueType.NOTES

        entry_command = ToggleEntryCommand(self.cell_controller, 5)
        entry_command.execute()
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)

        clear_command = ClearCellCommand(self.cell_controller)
        clear_command.execute()
        self.assertIsNone(self.cell_model.value)
        self.assertFalse(any(self.cell_model.notes))
        self.assertEqual(self.cell_model.value_type, CellValueType.BLANK)
        self.assertEqual(self.cell_model.notes, [False] * 9)

        clear_command.undo()
        self.assertEqual(self.cell_model.value, 5)
        self.assertEqual(self.cell_model.value_type, CellValueType.ENTRY)
        self.assertEqual(self.cell_model.notes, [True] * 3 + [False] * 6)

        entry_command.undo()
        self.assertEqual(self.cell_model.value, None)
        self.assertEqual(self.cell_model.value_type, CellValueType.NOTES)


class TestCommandHighlighting(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.root.withdraw()
        self.board_view = BoardView(self.root)
        self.board_controller = BoardController(self.root, MagicMock())

        # Ensure an empty board
        solver = BacktrackingSolver(self.board_controller)
        solver.has_unique_solution = Mock(return_value=True)
        generator = SudokuGenerator(self.board_controller, hint_manager=Mock(), timer=Mock(), solver=solver,
                                         target_count=81)
        generator.generate_board()
        self.conflict_observer = ConflictObserver(self.board_controller.model)
        self.show_number_buttons = NumberButton.show_number_buttons
        NumberButton.show_number_buttons = Mock()

        # For each test, we need a fresh cell controller and model
        self.cell_controller00 = self.board_controller.cells[0][0]  # Get a reference to a cell controller
        self.cell_controller01 = self.board_controller.cells[0][1]  # Get a reference to a cell controller
        self.cell_model = self.cell_controller00.model

    def tearDown(self):
        self.root.update_idletasks()
        time.sleep(0.1)
        self.root.destroy()
        NumberButton.show_number_buttons = self.show_number_buttons

    def test_undoing_restores_conflicts(self):
        """ Makes sure that if the user makes a conflict, clears, then undoes that, the conflict is restored. """
        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()
        command = ToggleEntryCommand(self.cell_controller01, 5)
        command.execute()

        self.assertTrue(self.cell_model.in_conflict)

        command = ClearCellCommand(self.cell_controller00)
        command.execute()
        self.assertFalse(self.cell_model.in_conflict)

        command.undo()
        self.assertTrue(self.cell_model.in_conflict)

    def test_undoing_removes_conflicts(self):
        """ Makes sure that if the user makes a conflict, then hits undo, the conflict is reversed. """
        command = ToggleEntryCommand(self.cell_controller00, 4)
        command.execute()
        command = ToggleEntryCommand(self.cell_controller01, 5)
        command.execute()
        self.assertFalse(self.cell_model.in_conflict)

        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()

        self.assertTrue(self.cell_model.in_conflict)

        command.undo()
        self.conflict_observer.update()
        self.assertFalse(self.cell_model.in_conflict)

    def test_redoing_restores_conflicts(self):
        """ If the user is in the conflict, hits undo then redo, this makes sure the conflict is restored. """
        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()
        command = ToggleEntryCommand(self.cell_controller01, 5)
        command.execute()

        self.assertTrue(self.cell_model.in_conflict)

        command.undo()
        self.assertFalse(self.cell_model.in_conflict)

        command.redo()
        self.assertTrue(self.cell_model.in_conflict)

    def test_redoing_removes_conflicts(self):
        """ Makes sure that if they undo into a state of conflict, they can redo if no more conflicts exist. """
        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()
        command = ToggleEntryCommand(self.cell_controller01, 5)
        command.execute()

        self.assertTrue(self.cell_model.in_conflict)

        command = ToggleEntryCommand(self.cell_controller01, 4)
        command.execute()
        self.assertFalse(self.cell_model.in_conflict)

        command.undo()
        self.conflict_observer.update()
        self.assertTrue(self.cell_model.in_conflict)

        command.redo()
        self.conflict_observer.update()
        self.assertFalse(self.cell_model.in_conflict)

    def test_clear_command_updates_number_buttons_undo_redo(self):
        """ Tests that undoing and redoing the clear command will trigger the number buttons to refresh. """
        command = ClearCellCommand(self.cell_controller00)
        command.execute()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.undo()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.redo()
        self.assertTrue(NumberButton.show_number_buttons.call_count > 0)

    def test_note_command_updates_number_buttons_undo_redo(self):
        """ Ensures that the note command will trigger the number buttons to refresh. """
        command = ToggleNoteCommand(self.cell_controller00, 5)
        command.execute()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.undo()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.redo()
        self.assertTrue(NumberButton.show_number_buttons.call_count > 0)

    def test_entry_command_updates_number_buttons_undo_redo(self):
        """ Ensures that the entry command will trigger the number buttons to refresh. """
        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.undo()
        NumberButton.show_number_buttons.assert_called_once()

        NumberButton.show_number_buttons.reset_mock()
        command.redo()
        self.assertTrue(NumberButton.show_number_buttons.call_count > 0)

    def test_entry_command_resets_matching_undo_redo(self):
        """ Makes sure that entry command will reset cells properly. """
        self.board_controller.reset_cells = Mock()
        self.cell_controller00.reset_matching_cells = Mock()
        command = ToggleEntryCommand(self.cell_controller00, 5)
        command.execute()
        self.cell_controller00.reset_matching_cells.assert_called_once()

        command.undo()
        self.board_controller.reset_cells.assert_called_once()

        self.board_controller.reset_cells.reset_mock()
        command.redo()
        self.board_controller.reset_cells.assert_called_once()

    def test_clear_command_resets_matching_undo_redo(self):
        """ Makes sure that clear command will reset cells properly. """
        self.board_controller.reset_cells = Mock()
        self.cell_controller00.reset_matching_cells = Mock()
        command = ClearCellCommand(self.cell_controller00)
        command.execute()
        self.cell_controller00.reset_matching_cells.assert_called_once()

        command.undo()
        self.board_controller.reset_cells.assert_called_once()

        self.board_controller.reset_cells.reset_mock()
        command.redo()
        self.board_controller.reset_cells.assert_called_once()


if __name__ == '__main__':
    unittest.main()
