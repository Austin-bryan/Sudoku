# Sudoku Game

## Overview
This project is a Python-based implementation of a Sudoku puzzle game, featuring a highly interactive and customizable user interface. The application is designed to provide a smooth and engaging experience, whether you're a seasoned Sudoku player or a beginner.

## Features
- **Dynamic Board Creation**: The game dynamically generates Sudoku puzzles with unique solutions, varying in difficulty.
- **Interactive UI**: The game uses a visually appealing and responsive graphical interface built with Tkinter.
- **Conflict Detection**: Real-time conflict detection highlights cells with conflicting numbers.
- **Hints and Assistance**: A hint system helps players by suggesting correct moves.
- **Undo/Redo**: A comprehensive undo/redo system allows players to revert or reapply their moves.
- **Timer**: Tracks the time taken to solve each puzzle.

## File Structure
### Controllers

**board_controller.py**: Manages the overall game logic, handling interactions between the model and the view.
**cell_controller.py**: Manages individual cell interactions, including number toggling, selection, and state updates.
Models

**board_model.py**: Represents the state of the Sudoku board, including cell values and their conflicts.
**cell_model.py**: Represents individual cell states, including notes and entries.
Views

**board_view.py**: Handles the visual representation of the Sudoku board.
**cell_view.py**: Manages the appearance and behavior of individual cells on the board.
number_button.py, action_button.py, toggle_button.py: Custom button widgets for interacting with the Sudoku grid.

### Utilities

**constants.py**: Contains constants used throughout the application, such as board size and colors.
**timer.py**: Implements a game timer that starts when the first cell is selected and stops when the puzzle is solved.
**backtracking_solver.py**: Implements a backtracking algorithm for solving the Sudoku puzzle programmatically.
**sudoku_generator.py**: Handles the generation of Sudoku boards with unique solutions.

### Observers

**board_start_observer.py, board_end_observer.py, conflict_observer.py, is_solved_observer.py**: Implements the observer pattern to manage game events, such as starting, detecting conflicts, and solving the puzzle.

### Command Pattern

**command.py**: Defines the base command interface for executing, undoing, and redoing operations.
**cell_commands.py**: Implements specific commands for cell interactions, such as toggling entries or notes.
**undo_history_manager.py**: Manages the history of commands for supporting undo and redo functionality.

### Testing

Includes comprehensive unit tests for all major components, ensuring reliability and correctness.

## Installation
To run this project, ensure you have Python installed along with the necessary dependencies:

```
pip install -r requirements.txt
```

## Usage
To start the game, simply run:

```
python main.py
```

## How to Play
- Select a cell on the board.
- Choose a number using the buttons or your keyboard.
- Use the hints feature if you're stuck.
- Keep an eye on the timer and try to solve the puzzle as quickly as possible.
- If you make a mistake, use the undo feature to correct it. You can also use redo to repeat. There's an unlimted number of undos.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or features you'd like to add.
