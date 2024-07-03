from controllers.cell_controller import CellController
from views.mode_button import ModeButton, Mode


class HintManager:
    """
    Tracks cells that had their values removed during the generation process.
    Randomly turns them back on for a hint.
    """
    def __init__(self):
        self.removed_values_cache = []

    def clear_cache(self):
        """ Clears the cache of removed values. """
        self.removed_values_cache = []

    def cache_removed_value(self, cell: CellController, value: int):
        """ Cache the removed value of a cell from the generation. """
        self.removed_values_cache.append((cell, value))

    def restore_hint(self):
        """ Restores a previously removed number to make a cell correct. """
        i = 0

        while True:
            if not self.removed_values_cache or i >= len(self.removed_values_cache):
                return
            cell, value = self.removed_values_cache[i]

            # Selects a cell either all notes, blank, or an incorrect entry
            if cell.model.is_notes() or cell.model.is_blank() or (cell.model.is_entry() and cell.model.in_conflict):
                self.removed_values_cache.pop(i)
                break

            i += 1

        cell.clear()

        # Cache old mode to return to later
        old_mode = ModeButton.mode
        ModeButton.mode = Mode.ENTRY
        cell.toggle_number(value)

        ModeButton.mode = old_mode
