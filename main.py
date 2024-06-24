import tkinter as tk
from typing import Union, Tuple
from controllers.board_controller import BoardController
from observers.conflict_observer import ConflictObserver
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BACKGROUND_COLOR, BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator
from views.action_button import ActionButton, DEFAULT_WIDTH
from views.number_button import NumberButton
from views.mode_button import ModeButton


class SudokuApp:
    def __init__(self, root):
        """Initialize the Sudoku application."""
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.grid_frame = SudokuApp.create_frame(self.root, row=0, column=0, padx=10, pady=10)  # Frame for Sudoku grid
        self.side_frame = SudokuApp.create_frame(self.root, row=0, column=1, padx=0, pady=0)  # Stores side buttons
        self.number_grid = SudokuApp.create_frame(self.side_frame, row=1, column=0, pady=(10, 0))  # Grid for number buttons
        self.bottom_row = SudokuApp.create_frame(self.side_frame, row=2, column=0, pady=(10, 0))  # Bottom row for buttons

        self.board_controller = BoardController(self.grid_frame)
        self.create_widgets()

        # Initialize BoardController
        self.board_controller.view.grid(row=0, column=0)
        generator = SudokuGenerator(self.board_controller)
        generator.generate_board()

    def create_widgets(self):
        """Create and configure the widgets for the Sudoku application."""

        # Create the grid of number buttons
        for i in range(BOARD_SIZE):
            number_button = NumberButton(self.number_grid, self.board_controller, i + 1)
            number_button.grid(row=i % 3, column=int(i / 3), padx=5, pady=5)

        # Attach the conflict observer
        conflict_observer = ConflictObserver(self.board_controller.model)
        backtracking_solver = BacktrackingSolver(self.board_controller)

        # Create action buttons
        padx = 2
        self.create_action_button('Undo', 0, lambda event: self.board_controller.clear_selected(), padx)
        self.create_action_button('Redo', 1, lambda event: self.board_controller.clear_selected(), padx)
        self.create_mode_button('Notes', 2, padx)
        self.create_action_button('Clear', 3, lambda event: self.board_controller.clear_selected(), padx)
        self.create_action_button('Hint', 4, lambda event: self.board_controller.clear_selected(), padx)

        # Create large buttons
        self.create_large_button('New Game', row=0, pady=0, command=lambda event: self.board_controller.clear_selected())
        self.create_large_button('Solve', row=3, pady=10, command=lambda event: backtracking_solver.solve())

    @staticmethod
    def create_frame(side_panel_frame, row, column,
                     padx: Union[int, Tuple[int, int]] = 0, pady: Union[int, Tuple[int, int]] = 0):
        frame = tk.Frame(side_panel_frame, bg=BACKGROUND_COLOR)
        frame.grid(row=row, column=column, padx=padx, pady=pady)
        return frame

    def create_large_button(self, label, row, pady, command):
        button = ActionButton(self.side_frame, label, width=320, font_size=15, height=DEFAULT_WIDTH, command=command)
        button.grid(row=row, column=0, pady=pady)

    def create_action_button(self, label, column, command, padx):
        """ Helper function to create an action button with an image. """
        button = ActionButton(self.bottom_row, label=label, image_path=label.lower() + '.png', command=command)
        button.grid(row=1, column=column, padx=padx, pady=5)

    def create_mode_button(self, label, column, padx):
        """ Helper function to create a mode button. """
        button = ModeButton(self.bottom_row, self.board_controller, label=label)
        button.grid(row=1, column=column, padx=padx, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
