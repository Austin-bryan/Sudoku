import unittest
from undo_history.undo_history_manager import UndoHistoryManager
from unittest.mock import MagicMock


class TestUndoHistoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = UndoHistoryManager()

    def test_execute_command_adds_to_history(self):
        """ Tests that execute command adds to history and executes properly. """
        command1 = MagicMock()
        self.manager.execute_command(command1)
        self.assertEqual(len(self.manager.history), 1)
        self.assertEqual(self.manager.current_index, 0)
        command1.execute.assert_called_once()

        command2 = MagicMock()
        self.manager.execute_command(command2)
        self.assertEqual(len(self.manager.history), 2)
        self.assertEqual(self.manager.current_index, 1)
        command2.execute.assert_called_once()

    def test_undo_reverts_to_previous_state(self):
        """ Asserts that undo winds the current index back by one index and calls the undo function. """
        command1 = MagicMock()
        command2 = MagicMock()
        self.manager.execute_command(command1)
        self.manager.execute_command(command2)
        self.manager.undo()
        self.assertEqual(self.manager.current_index, 0)
        command2.undo.assert_called_once()

    def test_redo_reapplies_command(self):
        """ Makes sure that redo is called properly. """
        command1 = MagicMock()
        command2 = MagicMock()
        self.manager.execute_command(command1)
        self.manager.execute_command(command2)
        self.manager.undo()
        self.manager.redo()
        self.assertEqual(self.manager.current_index, 1)
        command2.redo.assert_called_once()

    def test_clear_redo_history_on_new_command(self):
        """ Makes sure that when undoing, then executing a new command, the forward redo history is cleared. """
        command1 = MagicMock()
        command2 = MagicMock()
        command3 = MagicMock()
        self.manager.execute_command(command1)
        self.manager.execute_command(command2)
        self.manager.undo()
        self.manager.undo()
        self.manager.execute_command(command3)
        self.assertEqual(len(self.manager.history), 1)
        self.assertEqual(self.manager.current_index, 0)
        command1.undo.assert_called_once()
        command2.undo.assert_called_once()
        command3.execute.assert_called_once()
        self.assertNotIn(command2, self.manager.history)
        self.assertNotIn(command1, self.manager.history)

    def test_no_undo_beyond_initial_state(self):
        """ Makes sure there's no undo history beyond the initial state. """
        self.manager.undo()
        self.manager.undo()
        self.assertEqual(self.manager.current_index, -1)

    def test_no_redo_beyond_last_state(self):
        """ Makes sure there's no redo history beyond the last state. '"""
        command = MagicMock()
        self.manager.execute_command(command)
        self.manager.redo()  # Should not change state
        self.manager.redo()  # Should not change state
        self.assertEqual(self.manager.current_index, 0)


if __name__ == '__main__':
    unittest.main()
