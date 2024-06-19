# board_controller.py
from models.board_model import BoardModel
from views.board_view import BoardView
from controllers.cell_controller import CellController


class BoardController:
    def __init__(self, parent):
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cells = []
        self.selected_cell: CellController = None

        for x in range(9):
            row_controllers = []
            for y in range(9):
                cell_controller = CellController(self, self.view, self.model, x, y)
                row_controllers.append(cell_controller)
            self.cells.append(row_controllers)

    def populate_board(self, numbers):
        self.model.populate_board(numbers)
        for x in range(9):
            for y in range(9):
                value = self.model.get_cell_value(x, y)
                self.cells[x][y].view.update_labels()

    @property
    def cells_flat(self):
        return [cell for row in self.cells for cell in row]

    @staticmethod
    def clear_selected():
        if CellController.selected_cell:
            CellController.selected_cell.clear()

    def toggle_selected_cell(self, number):
        if self.selected_cell is not None and not self.selected_cell.model.is_given():
            self.selected_cell.toggle_number(number)

    def get_frame(self):
        return self.view.get_frame()
