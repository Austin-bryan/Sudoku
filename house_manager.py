from utils.constants import BOARD_SIZE, SUBGRID_SIZE


class HouseManager:
    def __init__(self, cell, board):
        self.cell = cell
        self.board = board

    def get_house(self):
        return self.get_row() + self.get_column() + self.get_subgrid()

    def get_row(self):
        return [self.board.cells[self.cell.x][y]
                for y in range(BOARD_SIZE)
                if y != self.cell.y]

    def get_column(self):
        return [self.board.cells[x][self.cell.y]
                for x in range(BOARD_SIZE)
                if x != self.cell.x]

    def get_subgrid(self):
        start_x = (self.cell.x // SUBGRID_SIZE) * SUBGRID_SIZE
        start_y = (self.cell.y // SUBGRID_SIZE) * SUBGRID_SIZE
        return [self.board.cells[i][j]
                for i in range(start_x, start_x + SUBGRID_SIZE)
                for j in range(start_y, start_y + SUBGRID_SIZE)
                if (i, j) != (self.cell.x, self.cell.y)]
