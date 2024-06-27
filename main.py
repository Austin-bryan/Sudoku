import tkinter as tk
from typing import Union, Tuple
from controllers.board_controller import BoardController
from observers.conflict_observer import ConflictObserver
from undo_history.undo_history_manager import UndoHistoryManager
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BACKGROUND_COLOR, BOARD_SIZE
from utils.sudoku_generator import SudokuGenerator
from views.action_button import ActionButton, DEFAULT_WIDTH
from views.drop_down_menu import DropdownMenu
from views.number_button import NumberButton
from views.mode_button import ModeButton


class SudokuApp:
    _PADX = (0, 20)

    def __init__(self, root):
        """Initialize the Sudoku application."""
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.grid_frame = self.create_frame(self.root, row=1, column=0, padx=10, pady=0)
        self.side_frame = self.create_frame(self.root, row=1, column=1, padx=0, pady=0)
        self.difficult_row = self.create_frame(self.side_frame, row=0, column=0, sticky="w")
        self.number_grid = self.create_frame(self.side_frame, row=3, column=0, padx=SudokuApp._PADX, pady=(10, 0))
        self.bottom_row = self.create_frame(self.side_frame, row=4, column=0, padx=SudokuApp._PADX, pady=(10, 0))

        self.undo_history_manager = UndoHistoryManager()
        self.board_controller = BoardController(self.grid_frame, self.undo_history_manager)
        self.create_widgets()

        # Initialize BoardController
        self.board_controller.view.grid(row=0, column=0)

        # Attach the conflict observer
        self.conflict_observer = ConflictObserver(self.board_controller.model)
        self.backtracking_solver = BacktrackingSolver(self.board_controller, ui_display_mode=True)

        # Create Difficulty UI
        self.difficulty_label = tk.Label(self.difficult_row, text="Difficulty:", bg=BACKGROUND_COLOR,
                                         fg="white", font=("Helvetica", 12), anchor="w")
        self.generator = None

        def easy_command(event):
            self.generator = SudokuGenerator(self.board_controller, 40)
            self.generator.generate_board()

        def medium_command(event):
            self.generator = SudokuGenerator(self.board_controller, 45)
            self.generator.generate_board()

        def hard_command(event):
            self.generator = SudokuGenerator(self.board_controller, 50)
            self.generator.generate_board()

        def extreme_command(event):
            self.generator = SudokuGenerator(self.board_controller, 55)
            self.generator.generate_board()

        easy_command(None)

        options = [("Easy", easy_command), ("Medium", medium_command), ("Hard", hard_command), ("Extreme", extreme_command)]

        dropdown = DropdownMenu(self.difficult_row, options, width=125, height=40)
        dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    def create_widgets(self):
        """Create and configure the widgets for the Sudoku application."""

        # Create the grid of number buttons
        for i in range(BOARD_SIZE):
            number_button = NumberButton(self.number_grid, self.board_controller, i + 1)
            number_button.grid(row=i % 3, column=int(i / 3), padx=5, pady=5)

        # Create action buttons
        padx = 2
        self.create_action_button('Undo', 0, lambda e: self.undo_history_manager.undo(), padx)
        self.create_action_button('Redo', 1, lambda e: self.undo_history_manager.redo(), padx)
        self.create_mode_button('Notes', 2, padx)
        self.create_action_button('Clear', 3, lambda e: self.board_controller.clear_selected(), padx)
        self.create_action_button('Hint', 4, lambda e: self.board_controller.clear_selected(), padx)

        # Create large buttons
        self.create_large_button('New Game', row=1, pady=0, command=lambda e: self.generator.generate_board())
        self.create_large_button('Solve', row=5, pady=10, command=lambda e: self.backtracking_solver.solve())

    @staticmethod
    def create_frame(parent, row, column,
                     padx: Union[int, Tuple[int, int]] = 0, pady: Union[int, Tuple[int, int]] = 0,
                     sticky: str = ""):
        frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        return frame

    def create_large_button(self, label, row, pady, command):
        button = ActionButton(self.side_frame, label, width=320, font_size=15, height=DEFAULT_WIDTH, command=command)
        button.grid(row=row, column=0, padx=SudokuApp._PADX, pady=pady)
        return button

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
