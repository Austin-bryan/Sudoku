﻿from models.board_model import BoardModel
from utils.constants import BOARD_SIZE
from views.board_view import BoardView
from controllers.cell_controller import CellController
import logging


class BoardController:
    """ Controller for managing the board's logic and interaction between the model and view. """

    def __init__(self, parent, undo_history_manager):
        """ Initialize the BoardController with a BoardModel, BoardView, and CellControllers. """
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cells = []
        self.parent = parent
        self.selected_cell: CellController = None
        self._undo_history_manager = undo_history_manager
        self._initialize_cells()
        self.can_select = True

    @property
    def undo_history_manager(self):
        return self._undo_history_manager

    def _initialize_cells(self):
        """ Initializes the cells in the board and assigns them to the view and model. """
        for x in range(BOARD_SIZE):
            row_controllers = []
            for y in range(BOARD_SIZE):
                try:
                    cell_controller = CellController(self, self.view, self.model, x, y)
                    row_controllers.append(cell_controller)
                except Exception as e:
                    logging.error(f"Error initializing cell at ({x}, {y}): {e}")
            self.cells.append(row_controllers)

    def populate_board(self, numbers):
        """ Populates the board with initial numbers and updates the view. """
        try:
            self.model.populate_board(numbers)
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    self.cells[x][y].view.update_labels()
        except Exception as e:
            logging.error(f"Error populating board: {e}")

    @property
    def cells_flat(self):
        """ Returns a flat list of all cell controllers on the board. """
        return [cell for row in self.cells for cell in row]

    def reset_cells(self):
        for cell in self.cells_flat:
            cell.view.reset_state()

    def clear_selected(self):
        """ Clears the currently selected cell if it exists. """
        if self.selected_cell:
            self.selected_cell.clear()

    def toggle_selected_cell(self, number):
        """
        Toggles the number for the currently selected cell if it is not a given cell.

        :param number: The number to toggle in the selected cell.
        """
        try:
            if self.selected_cell is not None and not self.selected_cell.model.is_given():
                self.selected_cell.toggle_number(number)
        except Exception as e:
            logging.error(f"Error toggling number in selected cell: {e}")

    def get_frame(self):
        return self.view.get_frame()

    def return_to_default(self):
        self.can_select = False

        for cell in self.cells_flat:
            cell.view.return_to_default()

    def select_cell(self, cell):
        if not self.can_select:
            return
        if self.selected_cell is not None:
            self.selected_cell.model.is_selected = False
        self.selected_cell = cell
        cell.model.is_selected = True
