from models.board_model import BoardModel
from utils.constants import BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator
from views.board_view import BoardView
from controllers.cell_controller import CellController
import logging


class BoardController:
    """
    Controller for managing the board's logic and interaction between the model and view.
    """

    def __init__(self, parent):
        """
        Initialize the BoardController with a BoardModel, BoardView, and CellControllers.

        :param parent: The parent GUI element.
        """
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cells = []
        self.selected_cell: CellController = None

        self._initialize_cells()

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
        """
        Populates the board with initial numbers and updates the view.

        :param numbers: A 2D list of numbers to be the sudoku board.
        """
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

    def clear_selected(self):
        """ Clears the currently selected cell if it exists. """
        try:
            if self.selected_cell:
                self.selected_cell.clear()
        except Exception as e:
            logging.error(f"Error clearing selected cell: {e}")

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
