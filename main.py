import tkinter as tk
from controllers.board_controller import BoardController
from observers.conflict_observer import ConflictObserver
from utils.constants import BACKGROUND_COLOR, BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator
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

        # Stores all buttons on the side
        side_panel_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        side_panel_frame.grid(row=0, column=1, padx=0, pady=0)

        # Grid for all 9 number buttons
        number_grid = tk.Frame(side_panel_frame, bg=BACKGROUND_COLOR)  # Set background color
        number_grid.grid(row=0, column=0, pady=(20, 0))  # Add some vertical space above the bottom row

        # Bottom row for extra buttons
        bottom_row = tk.Frame(side_panel_frame, bg=BACKGROUND_COLOR)
        bottom_row.grid(row=1, column=0, pady=(20, 0))

        # Initialize BoardController
        self.board_controller = BoardController(grid_frame)
        self.board_controller.view.grid(row=0, column=0)

        # Populate the board with some initial numbers for testing
        generator = SudokuGenerator()
        self.board_controller.populate_board(generator.generate_board())

        # Create the bottom row of buttons
        for i in range(BOARD_SIZE):
            number_button = NumberButton(number_grid, self.board_controller, i + 1)
            number_button.grid(row=i % 3, column=int(i / 3), padx=5, pady=5)

        mode_button = ModeButton(bottom_row, self.board_controller, label='M')
        mode_button.grid(row=4, column=4, padx=2, pady=5)

        delete_button = tk.Button(bottom_row, text='Delete', command=lambda: self.board_controller.clear_selected())
        delete_button.grid(row=0, column=10, padx=2, pady=5)

        # Optionally configure row and column weights to control resizing behavior
        for i in range(BOARD_SIZE):
            grid_frame.columnconfigure(i, weight=1)
            grid_frame.rowconfigure(i, weight=1)

        number_grid.columnconfigure(BOARD_SIZE, weight=1)

        conflict_observer = ConflictObserver(self.board_controller.model)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
