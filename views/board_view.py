import tkinter as tk
from utils.constants import BOARD_SIZE


class BoardView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(parent, bg='black')
        self.frame.grid(row=0, column=0, padx=5, pady=50)
        self.cells = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def add_cell_view(self, x, y, cell_view):
        self.cells[x][y] = cell_view
        cell_view.grid(row=x, column=y, padx=1, pady=1)

    def get_frame(self):
        return self.frame
