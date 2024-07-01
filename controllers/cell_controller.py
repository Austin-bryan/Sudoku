from controllers import board_controller
from house_manager import HouseManager
from models.board_model import BoardModel
from models.cell_model import CellModel
from undo_history.cell_commands import *
from undo_history.undo_history_manager import UndoHistoryManager
from utils.constants import BOARD_SIZE
from views.board_view import BoardView
from views.cell_view import CellView
from views.mode_button import ModeButton, Mode
from views.number_button import NumberButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.board_controller import BoardController


class CellController:
    """ Controller for managing the logic between the Cell Model and Cell View. """
    def __init__(self, board_controller: 'BoardController', board_view: BoardView, board_model: BoardModel,
                 x: int, y: int, **kwargs):
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            raise ValueError(f"Invalid cell coordinates: ({x}, {y})")

        self.model = CellModel(x, y)
        self.view = CellView(board_view.frame, self.model, **kwargs)
        self.board_controller = board_controller
        self.view.model = self.model

        # Set up house managers
        self.model.house_manager = HouseManager(self.model, board_model)
        self.view.house_manager = HouseManager(self.view, board_view)
        self.house_manager = HouseManager(self, board_controller)

        self.event_handler = EventHandler(self)
        self.highlighter = Highlighter(self, board_controller)
        self.selection_manager = SelectionManager(self)

        # Update the board model and view
        board_model.add_cell_model(x, y, self.model)
        board_view.add_cell_view(x, y, self.view)

    def select(self):
        """
        Called when the user either clicks on the cell, or uses the arrow keys to navigate.
        When this happens, the cell view is updated, to show its selected, and the house the cell belongs to is also
        highlighted.
        """
        if not self.board_controller.can_select:
            return
        self.board_controller.select_cell(self)
        self.board_controller.reset_cells()  # Clear any previous highlighting from the last selected cell
        self.view.focus_set()

        # Update Visuals
        self.highlighter.highlight_house()
        self.highlighter.highlight_matching_cells()
        self.view.enter_selected()
        NumberButton.show_number_buttons(self)

        # Notify the observers of the model
        self.board_controller.model.notify()

    def toggle_number(self, number: int):
        """
        Toggles a number on or off, depending on the mode. Givens cannot be toggled.
        Uses commands to have an undo history.
        :param number: The number that's being toggled on.
        """
        if self.model.is_given() or not self.board_controller.can_select:
            return
        if ModeButton.mode == Mode.ENTRY:
            command = ToggleEntryCommand(self, number)
            self.undo_history_manager.execute_command(command)
        else:
            command = ToggleNoteCommand(self, number)
            self.undo_history_manager.execute_command(command)

    def highlight_matching_cells(self):
        """ Highlights all cells with matching numbers. """
        if self.board_controller.can_select:
            self.highlighter.highlight_matching_cells()

    def clear(self, event=None):
        """ Executes a clear command, removing any entry and notes the cell had. """
        command = ClearCellCommand(self)
        self.undo_history_manager.execute_command(command)

    def highlight_house(self):
        """ Highlights all cells in the same house as the selected cell. """
        self.highlighter.highlight_house()

    def reset_matching_cells(self):
        """ Resets matching cells back to their default state, unless they are in conflict. """
        self.highlighter.reset_matching_cells()

    def move_selection(self, dx: int, dy: int):
        """
        Moves the selection some amount dx, dy, via the arrow keys.

        :param dx: Change in x.
        :param dy: Change in y.
        """
        self.selection_manager.move_selection(dx, dy)

    def get_house(self) -> list['CellController']:
        """ Returns all cells in the same row, column and subgrid as the selected cell. """
        return self.house_manager.get_house()

    def get_row(self) -> list['CellController']:
        """ Returns all cells in the same row as the selected cell. """
        return self.house_manager.get_row()

    def get_column(self) -> list['CellController']:
        """ Returns all cells in the same column as the selected cell. """
        return self.house_manager.get_column()

    def get_subgrid(self) -> list['CellController']:
        """ Returns all cells in the same subgrid as the selected cell. """
        return self.house_manager.get_subgrid()

    @property
    def undo_history_manager(self) -> UndoHistoryManager:
        """ Returns the undo history manager. """
        return self.board_controller.undo_history_manager

    @property
    def x(self) -> int:
        """ Return the X coordinate. """
        return self.model.x

    @x.setter
    def x(self, value):
        """ Set the X coordinate. """
        self.model.x = value

    @property
    def y(self) => int:
        """ Return the Y coordinate. """
        return self.model.y

    @y.setter
    def y(self, value):
        """ Set the Y coordinate. """
        self.model.y = value

    @property
    def value(self) -> int:
        """ Returns the cell value, whether it was given or entered. Notes do not count. """
        return self.model.value


class EventHandler:
    """ Handles the event binding for the cell controller. """
    def __init__(self, cell_controller):
        self.cell_controller = cell_controller
        self.view = cell_controller.view

        self.view.bind("<ButtonPress-1>", self.on_press)
        self.view.bind("<Up>", self.on_up)
        self.view.bind("<Down>", self.on_down)
        self.view.bind("<Left>", self.on_left)
        self.view.bind("<Right>", self.on_right)
        self.view.bind("<Key>", self.on_key_press)
        self.view.bind("<Delete>", self.clear)
        self.view.bind("<BackSpace>", self.clear)

    def on_press(self, event):
        """ Click event. """
        self.cell_controller.select()

    def on_up(self, event):
        """ Event for the up key. """
        self.cell_controller.move_selection(-1, 0)

    def on_down(self, event):
        """ Event for the down key. """
        self.cell_controller.move_selection(1, 0)

    def on_left(self, event):
        """ Event for the left key. """
        self.cell_controller.move_selection(0, -1)

    def on_right(self, event):
        """ Event for the right key. """
        self.cell_controller.move_selection(0, 1)

    def on_key_press(self, event):
        """ Makes sure only valid numeric keys are pressed. """
        if event.keysym in '123456789':
            self.cell_controller.toggle_number(int(event.keysym))
            self.cell_controller.highlight_matching_cells()

    def clear(self, event=None):
        self.cell_controller.clear()


class Highlighter:
    """ Manages the highlighting of the cell controller. """
    def __init__(self, cell_controller: CellController, board_controller: 'BoardController'):
        self.cell_controller = cell_controller
        self.board_controller = board_controller

    def highlight_matching_cells(self):
        """ Highlights all cells with matching numbers, even if in different houses. """
        matching_cells = self.get_matching_cells()
        for cell in matching_cells:
            cell.view.enter_matching()

    def highlight_house(self):
        """ Highlights all cells in the same house as the selected cell. """
        for cell in self.cell_controller.get_house():
            cell.view.enter_highlighted()

    def get_matching_cells(self) -> list[CellController]:
        """ Returns a list of all cells with the same value, not counting blacks or notes. """
        return [cell for cell in self.cell_controller.board_controller.cells_flat
                          if cell.model.value == self.cell_controller.model.value
                          and cell.model.has_value()
                          and cell.model is not self.cell_controller.model]

    def reset_matching_cells(self):
        """ Resets matching cells back to their default state, unless they're in conflict. """
        for cell in self.get_matching_cells():
            cell.view.reset_state()


class SelectionManager:
    def __init__(self, cell_controller):
        self.cell_controller = cell_controller

    def move_selection(self, dx: int, dy: int):
        """
        Selects the next cell based on dx and dy.
        Enables board wrapping if the selection is out of bounds
        :param dx: Change in X
        :param dy: Change in Y
        """

        new_x = (self.cell_controller.model.x + dx) % BOARD_SIZE
        new_y = (self.cell_controller.model.y + dy) % BOARD_SIZE
        new_cell = self.cell_controller.board_controller.cells[new_x][new_y]
        if new_cell:
            new_cell.event_handler.on_press(None)
