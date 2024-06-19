from models.cell_model import CellModel


class BoardModel:
    def __init__(self):
        self.cell_models = [[None for _ in range(9)] for _ in range(9)]

    def populate_board(self, numbers):
        for x in range(9):
            for y in range(9):
                if numbers[x][y] != 0:
                    self.cell_models[x][y].set_given(numbers[x][y])

    def get_cell_value(self, x, y):
        return self.cell_models[x][y].value

    def add_cell_model(self, x, y, cell_model):
        self.cell_models[x][y] = cell_model
