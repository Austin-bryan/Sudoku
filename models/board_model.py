﻿from models.cell_model import CellModel
from utils.constants import BOARD_SIZE


class BoardModel:
    def __init__(self):
        self.cell_models: list[list['CellModel']] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def populate_board(self, numbers):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if numbers[x][y] != 0:
                    self.cell_models[x][y].set_given(numbers[x][y])

    def get_cell_value(self, x, y):
        return self.cell_models[x][y].value

    def add_cell_model(self, x, y, cell_model):
        self.cell_models[x][y] = cell_model
