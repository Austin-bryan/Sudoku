from house_manager import HouseManager


class MockBoard:
    def __init__(self, board_controller):
        self.cells = [
            [MockCell(x, y, cell.model.value, self) for y, cell in enumerate(row)]
            for x, row in enumerate(board_controller.cells)
        ]


class MockCell:
    def __init__(self, x, y, value, board):
        self.x, self.y, self.value = x, y, value
        self.board = board
        self.house_manager = HouseManager(self, board)
        self.notes = [False] * 9

    def get_row(self):
        return self.house_manager.get_row()

    def get_column(self):
        return self.house_manager.get_column()

    def get_subgrid(self):
        return self.house_manager.get_subgrid()

    def get_house(self):
        return self.house_manager.get_house()
