from models.cell_model import CellModel


class BoardModel:
    def __init__(self):
        self.cell_models = [[None for _ in range(9)] for _ in range(9)]

    def populate_board(self, numbers):
        for x in range(9):
            for y in range(9):
                if numbers[x][y] != 0:
                    self.cell_models[x][y].add_entry(numbers[x][y])

    def get_cell_number(self, x, y):
        return self.cell_models[x][y].entry_number

    def set_cell(self, x, y, cell_model):
        self.cell_models[x][y] = cell_model