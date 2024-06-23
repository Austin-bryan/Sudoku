import random
from utils.constants import BOARD_SIZE, SUBGRID_SIZE


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def generate_board(self):
        self._fill_board()
        self._remove_numbers()
        return self.board

    def _fill_board(self):
        self._fill_diagonal()
        self._fill_remaining(0, SUBGRID_SIZE)

    def _fill_diagonal(self):
        for i in range(0, BOARD_SIZE, SUBGRID_SIZE):
            self._fill_box(i, i)

    def _fill_box(self, row, col):
        nums = list(range(1, BOARD_SIZE + 1))
        random.shuffle(nums)
        for i in range(SUBGRID_SIZE):
            for j in range(SUBGRID_SIZE):
                # self.board[row + i][col + j] = nums.pop()
                pass

    def _fill_remaining(self, x, y):
        # If column index 'y' goes beyond the last column and row index 'x' is less than BOARD_SIZE - 1,
        # move to the next row and reset 'y' to 0 (start of the row)
        if y >= BOARD_SIZE and x < BOARD_SIZE - 1:
            x += 1
            y = 0

        # Skip the cells that belong to the pre-filled blocks
        if x < SUBGRID_SIZE:
            if y < SUBGRID_SIZE:
                y = SUBGRID_SIZE  # Skip the first SUBGRID_SIZExSUBGRID_SIZE block
        elif x < 2 * SUBGRID_SIZE:
            if y == (x // SUBGRID_SIZE) * SUBGRID_SIZE:
                y += SUBGRID_SIZE  # Skip the middle SUBGRID_SIZExSUBGRID_SIZE block
        else:
            if y == 2 * SUBGRID_SIZE:
                x += 1  # Move to the next row if the current block is skipped
                y = 0
                if x >= BOARD_SIZE:
                    return True

        # Try filling the current cell with numbers 1 to BOARD_SIZE
        for num in range(1, BOARD_SIZE + 1):
            if self._is_safe(x, y, num):  # Check if it's safe to place 'num' in cell (x, y)
                self.board[x][y] = num  # Place 'num' in the cell
                if self._fill_remaining(x, y + 1):  # Recursively fill the next cell
                    return True
                self.board[x][y] = 0  # Reset the cell if it leads to a dead-end

        return False  # Return False if no valid number can be placed in the current cell

    # Returns true if it's unused
    def _is_safe(self, i, j, num):
        return (self._is_unused_in_row(i, num) and
                self._is_unused_in_col(j, num) and
                self._is_unused_in_box(i - i % SUBGRID_SIZE, j - j % SUBGRID_SIZE, num))

    def _is_unused_in_row(self, i, num):
        for j in range(BOARD_SIZE):
            if self.board[i][j] == num:
                return False
        return True

    def _is_unused_in_col(self, j, num):
        for i in range(BOARD_SIZE):
            if self.board[i][j] == num:
                return False
        return True

    def _is_unused_in_box(self, row_start, col_start, num):
        for i in range(SUBGRID_SIZE):
            for j in range(SUBGRID_SIZE):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def _remove_numbers(self):
        count = 40  # For difficulty, adjust the count
        while count != 0:
            i = random.randint(0, BOARD_SIZE - 1)
            j = random.randint(0, BOARD_SIZE - 1)
            while self.board[i][j] == 0:
                i = random.randint(0, BOARD_SIZE - 1)
                j = random.randint(0, BOARD_SIZE - 1)
            self.board[i][j] = 0
            count -= 1
