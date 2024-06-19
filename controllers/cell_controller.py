# controller/cell_controller.py
from models.cell_model import CellModel
from models.cell_value_type import CellValueType
from views.cell_view import CellView
from toggle_buttons import ModeButton, NumberButton, Mode


class CellController:
    # Initialize the board as a class attribute
    board: list[list['CellController']] = [[None for _ in range(9)] for _ in range(9)]
    selected_cell = None

    def __init__(self, board_view, board_model, x, y, **kwargs):
        self.model = CellModel(x, y)
        self.view = CellView(board_view.frame, self.model, **kwargs)
        self.view.model = self.model
        self.view.bind("<ButtonPress-1>", self.on_press)
        self.view.bind("<Up>", self.on_up)
        self.view.bind("<Down>", self.on_down)
        self.view.bind("<Left>", self.on_left)
        self.view.bind("<Right>", self.on_right)
        self.view.bind("<Key>", self.on_key_press)
        self.view.bind("<Delete>", self.clear)
        self.view.bind("<BackSpace>", self.clear)

        CellController.board[x][y] = self  # Store reference in the class attribute

        # Update the board model and view
        board_model.set_cell(x, y, self.model)
        board_view.add_cell_view(x, y, self.view)

    def on_press(self, event):
        CellController.selected_cell = self
        self.view.focus_set()
        for cell in CellController.all_cells():
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._DEFAULT_COLOR)
            else:
                cell.view.update_color(CellView._CONFLICT_COLOR)
        self.view.update_color(CellView._PRESS_COLOR)
        self.highlight_house()
        self.highlight_matching_numbers()
        self.show_number_buttons()

    def on_up(self, event):
        self.move_selection(-1, 0)

    def on_down(self, event):
        self.move_selection(1, 0)

    def on_left(self, event):
        self.move_selection(0, -1)

    def on_right(self, event):
        self.move_selection(0, 1)

    def on_key_press(self, event):
        if event.keysym not in '123456789':
            return
        self.toggle_number(int(event.keysym))

    def toggle_number(self, number):
        number = int(number)
        if self.model.is_given():
            return
        if ModeButton.mode == Mode.ENTRY:
            self.model.toggle_entry(number)
        else:
            self.model.toggle_note(number)
        self.view.update_labels()
        self.show_number_buttons()

    def highlight_matching_numbers(self):
        matching_cells = [cell for cell in CellController.all_cells()
                          if cell.model.value == self.model.value
                          and (cell.model.has_value() or cell.model.value_type == CellValueType.ENTRY)
                          and cell.model is not self.model]
        for cell in matching_cells:
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._MATCHING_COLOR)

    def clear(self, event):
        self.model.clear()
        if self.model.is_entry():
            pass
            # self.update_house_conflict_status()
        self.view.update_labels()

    def show_number_buttons(self):
        NumberButton.toggle_all_off()
        if ModeButton.mode == Mode.ENTRY:
            NumberButton.toggle_entry_on(self.model.value)
        elif ModeButton.mode == Mode.NOTES:
            NumberButton.toggle_note_on(self.model.notes)

    def highlight_house(self):
        for cell in self.get_house():
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._HIGHLIGHT_COLOR)
            cell.view._is_highlighted = True

    def move_selection(self, dx, dy):
        new_x = (self.model.x + dx) % 9
        new_y = (self.model.y + dy) % 9
        new_cell = CellController.board[new_x][new_y]
        if new_cell:
            new_cell.on_press(None)

    def get_house(self):
        return self.get_row() + self.get_column() + self.get_square()

    def get_row(self):
        return [CellController.board[self.model.x][y] for y in range(9) if CellController.board[self.model.x][y] is not self]

    def get_column(self):
        return [CellController.board[x][self.model.y] for x in range(9) if CellController.board[x][self.model.y] is not self]

    def get_square(self):
        start_x = (self.model.x // 3) * 3
        start_y = (self.model.y // 3) * 3
        return [CellController.board[i][j] for i in range(start_x, start_x + 3) for j in range(start_y, start_y + 3) if CellController.board[i][j] is not self]

    @classmethod
    def all_cells(cls):
        return [cell for row in cls.board for cell in row]

    @classmethod
    def toggle_selected_cell(cls, number):
        if cls.selected_cell is not None and not cls.selected_cell.model.is_given():
            cls.selected_cell.toggle_number(number)
