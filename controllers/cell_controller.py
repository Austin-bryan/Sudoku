from controllers import board_controller
from house_manager import HouseManager
from models.cell_model import CellModel
from undo_history.cell_commands import *
from utils.constants import BOARD_SIZE
from views.cell_view import CellView
from views.mode_button import ModeButton, Mode
from views.number_button import NumberButton


class CellController:
    def __init__(self, board_controller, board_view, board_model, x, y, **kwargs):
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            raise ValueError(f"Invalid cell coordinates: ({x}, {y})")

        self.model = CellModel(x, y)
        self.view = CellView(board_view.frame, self.model, **kwargs)
        self.board_controller = board_controller
        self.view.model = self.model
        self.model.house_manager = HouseManager(self.model, board_model)
        self.view.house_manager = HouseManager(self.view, board_view)

        self.event_handler = EventHandler(self)
        self.highlighter = Highlighter(self, board_controller)
        self.selection_manager = SelectionManager(self)
        self.house_manager = HouseManager(self, board_controller)

        # Update the board model and view
        board_model.add_cell_model(x, y, self.model)
        board_view.add_cell_view(x, y, self.view)

    def select(self):
        if self.board_controller.selected_cell is None:
            NumberButton.enable_all()
        self.board_controller.reset_cells()
        self.board_controller.selected_cell = self
        self.view.focus_set()

        self.highlighter.highlight_house()
        self.highlighter.highlight_matching_cells()
        self.view.enter_selected()
        NumberButton.show_number_buttons(self)

    def toggle_number(self, number):
        if self.model.is_given():
            return
        if ModeButton.mode == Mode.ENTRY:
            command = ToggleEntryCommand(self, number)
            self.undo_history_manager.execute_command(command)
        else:
            command = ToggleNoteCommand(self, number)
            self.undo_history_manager.execute_command(command)

    def highlight_matching_cells(self):
        self.highlighter.highlight_matching_cells()

    def clear(self, event=None):
        command = ClearCellCommand(self)
        self.undo_history_manager.execute_command(command)
        # self.board_controller.model.notify()

    def highlight_house(self):
        self.highlighter.highlight_house()

    def reset_matching_cells(self):
        self.highlighter.reset_matching_cells()

    def move_selection(self, dx, dy):
        self.selection_manager.move_selection(dx, dy)

    def get_house(self):
        return self.house_manager.get_house()

    def get_row(self):
        return self.house_manager.get_row()

    def get_column(self):
        return self.house_manager.get_column()

    def get_subgrid(self):
        return self.house_manager.get_subgrid()

    @property
    def undo_history_manager(self):
        return self.board_controller.undo_history_manager

    @property
    def x(self):
        return self.model.x

    @x.setter
    def x(self, value):
        self.model.x = value

    @property
    def y(self):
        return self.model.y

    @y.setter
    def y(self, value):
        self.model.y = value

    @property
    def value(self):
        return self.model.value


class EventHandler:
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
        self.cell_controller.select()

    def on_up(self, event):
        self.cell_controller.move_selection(-1, 0)

    def on_down(self, event):
        self.cell_controller.move_selection(1, 0)

    def on_left(self, event):
        self.cell_controller.move_selection(0, -1)

    def on_right(self, event):
        self.cell_controller.move_selection(0, 1)

    def on_key_press(self, event):
        if event.keysym in '123456789':
            self.cell_controller.toggle_number(int(event.keysym))
            self.cell_controller.highlight_matching_cells()

    def clear(self, event=None):
        self.cell_controller.clear()


class Highlighter:
    def __init__(self, cell_controller, board_control):
        self.cell_controller = cell_controller
        self.board_controller = board_control

    def highlight_matching_cells(self):
        matching_cells = self.get_matching_cells()
        for cell in matching_cells:
            cell.view.enter_matching()

    def highlight_house(self):
        for cell in self.cell_controller.get_house():
            cell.view.enter_highlighted()

    def get_matching_cells(self):
        return [cell for cell in self.cell_controller.board_controller.cells_flat
                          if cell.model.value == self.cell_controller.model.value
                          and cell.model.has_value()
                          and cell.model is not self.cell_controller.model]

    def reset_matching_cells(self):
        for cell in self.get_matching_cells():
            cell.view.reset_state()


class SelectionManager:
    def __init__(self, cell_controller):
        self.cell_controller = cell_controller

    def move_selection(self, dx, dy):
        new_x = (self.cell_controller.model.x + dx) % BOARD_SIZE
        new_y = (self.cell_controller.model.y + dy) % BOARD_SIZE
        new_cell = self.cell_controller.board_controller.cells[new_x][new_y]
        if new_cell:
            new_cell.event_handler.on_press(None)
