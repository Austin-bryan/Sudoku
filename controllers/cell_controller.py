from models.cell_model import CellModel
from utils.constants import BOARD_SIZE, SUBGRID_SIZE
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

        self.view.bind("<ButtonPress-1>", self.on_press)
        self.view.bind("<Up>", self.on_up)
        self.view.bind("<Down>", self.on_down)
        self.view.bind("<Left>", self.on_left)
        self.view.bind("<Right>", self.on_right)
        self.view.bind("<Key>", self.on_key_press)
        self.view.bind("<Delete>", self.clear)
        self.view.bind("<BackSpace>", self.clear)

        # Update the board model and view
        board_model.add_cell_model(x, y, self.model)
        board_view.add_cell_view(x, y, self.view)

    def on_press(self, event):
        if self.board_controller.selected_cell is None:
            NumberButton.enable_all()
        self.board_controller.selected_cell = self
        self.view.focus_set()

        for cell in self.board_controller.cells_flat:
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._DEFAULT_COLOR)
            else:
                cell.view.update_color(CellView._CONFLICT_COLOR)
        self.view.update_color(CellView._PRESS_COLOR)
        self.highlight_house()
        self.highlight_matching_numbers()
        NumberButton.show_number_buttons(self)

    def on_up(self, event):
        self._safe_move_selection(-1, 0)

    def on_down(self, event):
        self._safe_move_selection(1, 0)

    def on_left(self, event):
        self._safe_move_selection(0, -1)

    def on_right(self, event):
        self._safe_move_selection(0, 1)

    def on_key_press(self, event):
        if event.keysym in '123456789':
            self.toggle_number(int(event.keysym))
            self.highlight_matching_numbers()

    def toggle_number(self, number):
        if self.model.is_given():
            return
        if ModeButton.mode == Mode.ENTRY:
            self.model.toggle_entry(number)
            for cell in self.get_house():
                if cell.model.is_notes() and cell.model.has_note(number):
                    cell.model.toggle_note(number)
                    cell.view.update_labels()
        else:
            self.model.toggle_note(number)
        self.view.update_labels()
        NumberButton.show_number_buttons(self)

    def highlight_matching_numbers(self):
        matching_cells = [cell for cell in self.board_controller.cells_flat
                          if cell.model.value == self.model.value
                          and cell.model.has_value()
                          and cell.model is not self.model]
        for cell in matching_cells:
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._MATCHING_COLOR)

    def clear(self, event=None):
        self.model.clear_cell()
        self.view.update_labels()
        NumberButton.show_number_buttons(self)

    def highlight_house(self):
        for cell in self.get_house():
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._HIGHLIGHT_COLOR)
            cell.view._is_highlighted = True

    def move_selection(self, dx, dy):
        new_x = (self.model.x + dx) % BOARD_SIZE
        new_y = (self.model.y + dy) % BOARD_SIZE
        new_cell = self.board_controller.cells[new_x][new_y]
        if new_cell:
            new_cell.on_press(None)

    def _safe_move_selection(self, dx, dy):
        try:
            self.move_selection(dx, dy)
        except IndexError as e:
            print(f"Error during move selection: {e}")

    def get_house(self):
        return self.get_row() + self.get_column() + self.get_subgrid()

    def get_row(self):
        return [self.board_controller.cells[self.model.x][y]
                for y in range(BOARD_SIZE)
                if y != self.model.y]

    def get_column(self):
        return [self.board_controller.cells[x][self.model.y]
                for x in range(BOARD_SIZE)
                if x != self.model.x]

    def get_subgrid(self):
        start_x = (self.model.x // SUBGRID_SIZE) * SUBGRID_SIZE
        start_y = (self.model.y // SUBGRID_SIZE) * SUBGRID_SIZE
        return [self.board_controller.cells[i][j]
                for i in range(start_x, start_x + SUBGRID_SIZE)
                for j in range(start_y, start_y + SUBGRID_SIZE)
                if (i, j) != (self.model.x, self.model.y)]
