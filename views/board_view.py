import tkinter as tk
from views.cell_view import CellView
from colors import *


class BoardView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(parent, bg='black')
        self.frame.grid(row=0, column=0, padx=5, pady=50)
        self.cell_views = [[None for _ in range(9)] for _ in range(9)]

    def add_cell_view(self, x, y, cell_view):
        self.cell_views[x][y] = cell_view
        cell_view.grid(row=x, column=y, padx=1, pady=1)

    def get_frame(self):
        return self.frame