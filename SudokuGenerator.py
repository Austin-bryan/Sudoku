import random


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def generate_board(self):
        self._fill_board()
        self._remove_numbers()
        return self.board

    def _fill_board(self):
        self._fill_diagonal()
        self._fill_remaining(0, 3)

    def _fill_diagonal(self):
        for i in range(0, 9, 3):
            self._fill_box(i, i)

    def _fill_box(self, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()

    def _fill_remaining(self, x, y):
        # If column index 'y' goes beyond the last column and row index 'x' is less than 8,
        # move to the next row and reset 'y' to 0 (start of the row)
        if y >= 9 and x < 8:
            x += 1
            y = 0

        # If both row and column indices are beyond the last cell, the board is fully filled
        if x >= 9 and y >= 9:
            return True

        # Skip the cells that belong to the pre-filled blocks
        if x < 3:
            if y < 3:
                y = 3  # Skip the first 3x3 block
        elif x < 6:
            if y == (x // 3) * 3:
                y += 3  # Skip the middle 3x3 block
        else:
            if y == 6:
                x += 1  # Move to the next row if the current block is skipped
                y = 0
                if x >= 9:
                    return True

        # Try filling the current cell with numbers 1 to 9
        for num in range(1, 10):
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
                self._is_unused_in_box(i - i % 3, j - j % 3, num))

    def _is_unused_in_row(self, i, num):
        for j in range(9):
            if self.board[i][j] == num:
                return False
        return True

    def _is_unused_in_col(self, j, num):
        for i in range(9):
            if self.board[i][j] == num:
                return False
        return True

    def _is_unused_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def _remove_numbers(self):
        count = 40  # For difficulty, adjust the count
        while count != 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            while self.board[i][j] == 0:
                i = random.randint(0, 8)
                j = random.randint(0, 8)
            self.board[i][j] = 0
            count -= 1
