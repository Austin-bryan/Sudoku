from typing import Union, Tuple, Callable
import tkinter as tk
from tkinter import Event

from controllers.board_controller import BoardController
from models.cell_value_type import CellValueType
from observers.board_end_observer import BoardEndObserver
from observers.board_start_observer import BoardStartObserver
from observers.conflict_observer import ConflictObserver
from observers.is_solved_observer import IsSolvedObserver
from timer import Timer
from undo_history.undo_history_manager import UndoHistoryManager
from utils.backtracking_solver import BacktrackingSolver
from utils.constants import BACKGROUND_COLOR, BOARD_SIZE
from utils.hint_manager import HintManager
from utils.sudoku_generator import SudokuGenerator
from views.action_button import ActionButton, DEFAULT_WIDTH
from views.drop_down_menu import DropdownMenu
from views.number_button import NumberButton
from views.mode_button import ModeButton


class SudokuApp:
    PADX = (0, 20)

    def __init__(self, root):
        """Initialize the Sudoku application."""
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Create frames
        self.grid_frame = self.create_frame(self.root, row=1, column=0, padx=10, pady=0)
        self.side_frame = self.create_frame(self.root, row=1, column=1, padx=0, pady=0)
        self.top_row = self.create_frame(self.side_frame, row=0, column=0, sticky="w")
        self.number_grid = self.create_frame(self.side_frame, row=3, column=0, padx=SudokuApp.PADX, pady=(10, 0))
        self.bottom_row = self.create_frame(self.side_frame, row=4, column=0, padx=SudokuApp.PADX, pady=(10, 0))

        self.undo_history_manager = UndoHistoryManager()
        self.board_controller = BoardController(self.grid_frame, self.undo_history_manager)
        self.create_widgets()

        # Initialize BoardController
        self.board_controller.view.grid(row=0, column=0)

        # Create Difficulty UI
        self.difficulty_label = tk.Label(self.top_row, text="Difficulty:", bg=BACKGROUND_COLOR,
                                         fg="white", font=("Helvetica", 12), anchor="w")
        self.generator = None

        # Create timer
        self.timer = Timer(self.top_row)
        self.timer.grid(row=0, column=3, sticky="w", padx=5, pady=10)

        # Create observers
        self.conflict_observer = ConflictObserver(self.board_controller.model)
        self.is_solved_observer = IsSolvedObserver(self.board_controller.model)
        self.board_start_observer = BoardStartObserver(self.board_controller.model, self.timer)
        self.board_end_observer = BoardEndObserver(self.is_solved_observer, self.timer,
                                                   self.board_controller, self.board_start_observer)

        # Create other utility classes
        self.backtracking_solver = BacktrackingSolver(self.board_controller, ui_display_mode=True)
        self.hint_manager = HintManager()

        # Generate an easy board to start
        self.easy_command(None)

    # Commands for difficulty creation
    def easy_command(self, event: Event):
        """ Generate easy puzzle. """
        self.start_new_game(35)

    def medium_command(self, event: Event):
        """ Generate medium puzzle. """
        self.start_new_game(40)

    def hard_command(self, event: Event):
        """ Generate hard puzzle. """
        self.start_new_game(50)

    def start_new_game(self, target_count: int):
        """
        Creates a puzzle generator to use for new games. Clears old data from previous game.
        :param target_count: Determines how many cells will be cleared.
        """
        self.hint_manager.clear_cache()
        self.generator = SudokuGenerator(self.board_controller, self.hint_manager, self.timer, target_count)
        self.generator.generate_board()
        self.undo_history_manager.clear_history()

    def create_widgets(self):
        """ Create and configure the widgets for the Sudoku application. """

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
        self.create_action_button('Hint', 4, lambda e: self.hint_manager.restore_hint(), padx)

        # Create difficulty drop down menu
        options = [("Easy", self.easy_command), ("Medium", self.medium_command), ("Hard", self.hard_command)]

        dropdown = DropdownMenu(self.top_row, options, width=100, height=40)
        dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=10)

        # Create auto notes button
        auto_notes_button = ActionButton(self.top_row, 'Auto Notes', font_size=12,
                                         width=100, height=40, command=self.auto_notes_command)
        auto_notes_button.grid(row=0, column=2, sticky="w", padx=5, pady=10)

        # Create large buttons
        self.create_large_button('New Game', row=1, pady=0, command=self.new_game_command)
        self.create_large_button('Solve', row=5, pady=10, command=lambda e: self.backtracking_solver.solve())

    def auto_notes_command(self, event):
        """ Auto populates all cells with valid notes. """
        for cell in self.board_controller.cells_flat:

            # Get possible notes
            possible_values = list(range(1, BOARD_SIZE + 1))

            # Skip Given or Entries
            if cell.model.value_type is CellValueType.GIVEN or cell.model.value_type is CellValueType.ENTRY:
                continue

            # Clear any notes that are already there
            cell.model.clear()

            # Remove values that are already in the house
            for house_cell in cell.get_house():
                if house_cell.value in possible_values:
                    possible_values.remove(house_cell.value)

            # For all that remain, toggle the notes
            for possible_value in possible_values:
                cell.model.toggle_note(possible_value)

    def new_game_command(self, event):
        """ Generates a new board, reset all cells and states for a new game. """
        self.generator.generate_board()
        self.board_controller.return_to_default()
        self.board_controller.can_select = True
        self.board_start_observer.game_has_started = False

    @staticmethod
    def create_frame(parent, row: int, column: int,
                     padx: Union[int, Tuple[int, int]] = 0,
                     pady: Union[int, Tuple[int, int]] = 0, sticky: str = ""):
        """ Helper function for creating a frame. """
        frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        return frame

    def create_large_button(self, label: str, row: int, pady: int, command: Callable[[tk.Event], None]):
        """ Helper function for creating large buttons. """
        button = ActionButton(self.side_frame, label, width=320, font_size=15, height=DEFAULT_WIDTH, command=command)
        button.grid(row=row, column=0, padx=SudokuApp.PADX, pady=pady)
        return button

    def create_action_button(self, label, column, command, padx):
        """ Helper function to create a square action button with an image. """
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
