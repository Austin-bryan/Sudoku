from utils.constants import BOARD_SIZE, SUBGRID_SIZE


class HouseManager:
    """
    Given a cell and a board, allows the retrival of rows, columns, subgrids and houses.
    This is generalized to work with anything that supports the interface.
    """
    def __init__(self, cell: any, board: any):
        self.cell = cell
        self.board = board

    def get_row(self) -> list[any]:
        """ Returns all cells in the same row. """
        return [self.board.cells[self.cell.x][y]
                for y in range(BOARD_SIZE)
                if y != self.cell.y]

    def get_column(self) -> list[any]:
        """ Returns all cells in the same column. """
        return [self.board.cells[x][self.cell.y]
                for x in range(BOARD_SIZE)
                if x != self.cell.x]

    def get_subgrid(self) -> list[any]:
        """ Returns all cells in the same subgrid. A subgrid is the 3x3 area of the puzzle. """
        start_x = (self.cell.x // SUBGRID_SIZE) * SUBGRID_SIZE
        start_y = (self.cell.y // SUBGRID_SIZE) * SUBGRID_SIZE

        return [self.board.cells[i][j]
                for i in range(start_x, start_x + SUBGRID_SIZE)
                for j in range(start_y, start_y + SUBGRID_SIZE)
                if (i, j) != (self.cell.x, self.cell.y)]

    def get_house(self) -> list[any]:
        """ Returns all cells in the same house (row, column and subgrid). """
        return self.get_row() + self.get_column() + self.get_subgrid()
