# board_controller.py
from models.board_model import BoardModel
from utils.constants import BOARD_SIZE
from views.board_view import BoardView
from controllers.cell_controller import CellController


class BoardController:
    def __init__(self, parent):
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cells = []
        self.selected_cell: CellController = None

        for x in range(BOARD_SIZE):
            row_controllers = []
            for y in range(BOARD_SIZE):
                cell_controller = CellController(self, self.view, self.model, x, y)
                row_controllers.append(cell_controller)
            self.cells.append(row_controllers)

    def populate_board(self, numbers):
        self.model.populate_board(numbers)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.cells[x][y].view.update_labels()

    @property
    def cells_flat(self):
        return [cell for row in self.cells for cell in row]

    def clear_selected(self):
        if self.selected_cell:
            self.selected_cell.clear()

    def toggle_selected_cell(self, number):
        if self.selected_cell is not None and not self.selected_cell.model.is_given():
            self.selected_cell.toggle_number(number)

    def get_frame(self):
        return self.view.get_frame()
