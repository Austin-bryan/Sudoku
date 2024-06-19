# board_controller.py
from models.board_model import BoardModel
from views.board_view import BoardView
from controllers.cell_controller import CellController


class BoardController:
    def __init__(self, parent):
        self.model = BoardModel()
        self.view = BoardView(parent)
        self.cell_controllers = []

        for x in range(9):
            row_controllers = []
            for y in range(9):
                cell_controller = CellController(self.view, self.model, x, y)
                row_controllers.append(cell_controller)
            self.cell_controllers.append(row_controllers)

    def populate_board(self, numbers):
        self.model.populate_board(numbers)
        for x in range(9):
            for y in range(9):
                value = self.model.get_cell_value(x, y)
                self.cell_controllers[x][y].view.update_labels()

    @staticmethod
    def clear_selected():
        if CellController.selected_cell:
            CellController.selected_cell.clear()

    def get_frame(self):
        return self.view.get_frame()
