from models.board_model import BoardModel
from undo_history.undo_history_manager import UndoHistoryManager
from utils.constants import BOARD_SIZE
from views.board_view import BoardView
from controllers.cell_controller import CellController
import tkinter as tk
import logging


class BoardController:
    """ Controller for managing the board's logic and interaction between the model and view. """

    def __init__(self, parent: tk.Frame, undo_history_manager: UndoHistoryManager):
        """ Initialize the BoardController with a BoardModel, BoardView, and CellControllers. """
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cells = []
        self.parent = parent
        self.selected_cell: CellController = None
        self._undo_history_manager = undo_history_manager
        self._initialize_cells()
        self.can_select = True  # When false, disables the user from selecting cells

    @property
    def undo_history_manager(self) -> UndoHistoryManager:
        """ Returns the undo history manager instance. """
        return self._undo_history_manager

    def _initialize_cells(self):
        """ Initializes the cells in the board and assigns them to the view and model. """
        for x in range(BOARD_SIZE):
            row_controllers = []
            for y in range(BOARD_SIZE):
                try:
                    # Create and add cell controller
                    cell_controller = CellController(self, self.view, self.model, x, y)
                    row_controllers.append(cell_controller)
                except Exception as e:
                    logging.error(f"Error initializing cell at ({x}, {y}): {e}")
            self.cells.append(row_controllers)

    def populate_board(self, numbers: list[int]):
        """
        Populates the board with initial numbers and updates the view.

        :param numbers: the initial numbers
        """

        # Update the models
        self.model.populate_board(numbers)

        # Update the views
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.cells[x][y].view.update_labels()

    @property
    def cells_flat(self) -> list[CellController]:
        """ Returns a flat list of all cell controllers on the board. """
        return [cell for row in self.cells for cell in row]

    def reset_cells(self):
        """
        Resets all cells to their initial state, unless they are in conflict.
        This is used when a selection is changed to reset the colors.
        """
        for cell in self.cells_flat:
            cell.view.reset_state()

    def clear_selected(self):
        """ Clears the currently selected cell if it exists. """
        if self.selected_cell:
            self.selected_cell.clear()

    def toggle_selected_cell(self, number: int):
        """
        Toggles the number for the currently selected cell if it is not a given cell.

        :param number: The number to toggle in the selected cell.
        """
        try:
            if self.selected_cell is not None and not self.selected_cell.model.is_given():
                self.selected_cell.toggle_number(number)
        except Exception as e:
            logging.error(f"Error toggling number in selected cell: {e}")

    def return_to_default(self):
        """
        Resets all cells to their initial state, even if they are in conflict.
        This is used when a new game is made, so all previous states must be ignored.
        """
        self.can_select = False

        for cell in self.cells_flat:
            cell.view.return_to_default()

    def select_cell(self, cell: CellController):
        """ Deselects the old cell, and sets the new cell as selected. """
        if not self.can_select:
            return
        # Deselect old cell
        if self.selected_cell is not None:
            self.selected_cell.model.is_selected = False

        # Select new cell
        self.selected_cell = cell
        cell.model.is_selected = True
