from controllers.board_controller import BoardController
from house_manager import HouseManager


class MockBoard:
    """
    Designed to have a simplified interface compared to BoardController,
    allowing mutation of data without affecting the original board controller.
    """
    def __init__(self, board_controller: BoardController):
        self.cells = [
            [MockCell(x, y, cell.model.value, self) for y, cell in enumerate(row)]
            for x, row in enumerate(board_controller.cells)
        ]


class MockCell:
    """
    Designed to have a simplified interface compared to CellController,
    allowing mutation of dating without affecting the original cell controllers.
    """
    def __init__(self, x: int, y: int, value: int, board: MockBoard):
        self.x, self.y, self.value = x, y, value
        self.board = board
        self.house_manager = HouseManager(self, board)
        self.notes = [False] * 9

    def get_row(self):
        """ Returns the row of the cell. """
        return self.house_manager.get_row()

    def get_column(self):
        """ Returns the column of the cell. """
        return self.house_manager.get_column()

    def get_subgrid(self):
        """ Returns the subgrid of the cell. """
        return self.house_manager.get_subgrid()

    def get_house(self):
        """ Returns the house (row, column and subgrid) of the cell. """
        return self.house_manager.get_house()
