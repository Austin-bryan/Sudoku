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
                self.cell_controllers[x][y].view.update_hint(value)

    def clear_selected(self):
        if CellController.selected_cell:
            selected_cell = CellController.selected_cell
            if selected_cell.model.is_entry():
                selected_cell.model.clear_entry()
            else:
                selected_cell.model.clear_notes()
            selected_cell.view.update_color(CellView._DEFAULT_COLOR)
            selected_cell.update_house_conflict_status()

    def get_frame(self):
        return self.view.get_frame()
