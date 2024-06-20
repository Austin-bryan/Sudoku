import tkinter as tk
from controllers.board_controller import BoardController
from utils.colors import BACKGROUND_COLOR
from views.number_button import NumberButton
from views.mode_button import ModeButton


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.create_widgets()

    def create_widgets(self):
        # Frame for Sudoku grid
        grid_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)  # Set background color
        grid_frame.grid(row=0, column=0, padx=5, pady=50)

        # Frame for the bottom row of buttons
        bottom_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)  # Set background color
        bottom_frame.grid(row=1, column=0, pady=(20, 0))  # Add some vertical space above the bottom row

        # Initialize BoardController
        self.board_controller = BoardController(grid_frame)
        self.board_controller.view.grid(row=0, column=0)

        # Populate the board with some initial numbers for testing
        initial_numbers = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.board_controller.populate_board(initial_numbers)

        # Create the bottom row of buttons
        for i in range(9):
            number_button = NumberButton(bottom_frame, self.board_controller, i + 1)
            number_button.grid(row=0, column=i, padx=2, pady=5)  # Adjust padding here for more spread out buttons

        mode_button = ModeButton(bottom_frame, self.board_controller, label='M')
        mode_button.grid(row=0, column=9, padx=2, pady=5)

        delete_button = tk.Button(bottom_frame, text='Delete', command=lambda: self.board_controller.clear_selected())
        delete_button.grid(row=0, column=10, padx=2, pady=5)

        # Optionally configure row and column weights to control resizing behavior
        for i in range(9):
            grid_frame.columnconfigure(i, weight=1)
            grid_frame.rowconfigure(i, weight=1)

        bottom_frame.columnconfigure(9, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()