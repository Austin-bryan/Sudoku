from ToggleButtons import *
from Slot import *


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

        # Create a 9x9 grid of Slot widgets for the Sudoku board
        for i in range(9):
            for j in range(9):
                slot = Slot(grid_frame, x=i, y=j)  # Set slot background color and remove borders
                # Set slot background color
                slot.grid(row=i, column=j, padx=1, pady=1)  # Adjust padding here for compactness

        Slot.populate_board()

        # Create the bottom row of buttons
        for i in range(9):
            number_button = NumberButton(bottom_frame, number=str(i + 1))
            number_button.grid(row=0, column=i, padx=2, pady=5)  # Adjust padding here for more spread out buttons

        mode_button = ModeButton(bottom_frame, label='M')
        mode_button.grid(row=0, column=9, padx=2, pady=5)

        # Optionally configure row and column weights to control resizing behavior
        for i in range(9):
            grid_frame.columnconfigure(i, weight=1)
            grid_frame.rowconfigure(i, weight=1)

        bottom_frame.columnconfigure(9, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
