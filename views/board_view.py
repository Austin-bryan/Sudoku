import tkinter as tk
from typing import Union
from utils.constants import BOARD_SIZE
from views.cell_view import CellView


class BoardView(tk.Frame):
    """ Handles the visual of the board. """
    def __init__(self, parent: Union[tk, tk.Frame]):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(parent, bg='black')
        self.frame.grid(row=0, column=0, padx=5, pady=50)
        self.cells = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def add_cell_view(self, x: int, y: int, cell_view: CellView):
        """
        Cell Views are created by Cell Controllers,
        then they use this method to add themselves so the board view can track them.
        """
        self.cells[x][y] = cell_view
        cell_view.grid(row=x, column=y, padx=1, pady=1)

    def get_frame(self):
        return self.frame
