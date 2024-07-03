import unittest
from unittest.mock import MagicMock

from models.cell_model import CellModel
from utils.hint_manager import HintManager
from controllers.cell_controller import CellController
from models.cell_value_type import CellValueType
from views.mode_button import ModeButton, Mode


class TestHintManager(unittest.TestCase):

    def setUp(self):
        self.hint_manager = HintManager()
        self.cell_controller = MagicMock(spec=CellController)
        self.cell_controller.model = MagicMock(spec=CellModel)
        self.cell_controller.model.is_notes = MagicMock(return_value=False)
        self.cell_controller.model.is_blank = MagicMock(return_value=False)
        self.cell_controller.model.is_entry = MagicMock(return_value=True)
        self.cell_controller.model.is_given = MagicMock(return_value=False)
        self.cell_controller.model.in_conflict = True
        self.cell_controller.model.value = None

        self.cell_controller.clear = MagicMock()
        self.cell_controller.toggle_number = MagicMock()
        self.cell_controller.model.value_type = CellValueType.ENTRY
        ModeButton.mode = Mode.ENTRY

    def test_hints_override_notes(self):
        self.cell_controller.model.is_notes = MagicMock(return_value=True)
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.restore_hint()
        self.cell_controller.clear.assert_called_once()
        self.cell_controller.toggle_number.assert_called_once_with(5)

    def test_hints_ignore_givens(self):
        self.cell_controller.model.is_given = MagicMock(return_value=True)
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.restore_hint()
        self.cell_controller.clear.assert_not_called()
        self.cell_controller.toggle_number.assert_not_called()

    def test_hints_override_conflicted_cells(self):
        self.cell_controller.model.in_conflict = True
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.restore_hint()
        self.cell_controller.clear.assert_called_once()
        self.cell_controller.toggle_number.assert_called_once_with(5)

    def test_hints_can_fix_mistakes(self):
        self.cell_controller.model.value = 3
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.restore_hint()
        self.cell_controller.clear.assert_called_once()
        self.cell_controller.toggle_number.assert_called_once_with(5)

    def test_hints_restore_mode_button_type(self):
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        ModeButton.mode = Mode.NOTES
        self.hint_manager.restore_hint()
        self.assertEqual(ModeButton.mode, Mode.NOTES)

    def test_cache_cleared_on_new_game(self):
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.clear_cache()
        self.assertEqual(len(self.hint_manager.removed_values_cache), 0)

    def test_cache_updated_properly(self):
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.assertEqual(len(self.hint_manager.removed_values_cache), 1)
        self.assertEqual(self.hint_manager.removed_values_cache[0], (self.cell_controller, 5))

    def test_restore_hint_selects_cell(self):
        self.hint_manager.cache_removed_value(self.cell_controller, 5)
        self.hint_manager.restore_hint()
        self.cell_controller.select.assert_called_once()


if __name__ == '__main__':
    unittest.main()
