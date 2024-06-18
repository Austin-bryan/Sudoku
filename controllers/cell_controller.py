# controller/cell_controller.py
from models.cell_model import CellModel
from models.cell_value_type import CellValueType
from views.cell_view import CellView
from toggle_buttons import ModeButton, NumberButton, Mode


class CellController:
    selected_cell = None
    board = [[None for _ in range(9)] for _ in range(9)]  # Initialize the board as a class attribute

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
        self.view.bind("<Delete>", self.clear_selected)
        self.view.bind("<BackSpace>", self.clear_selected)

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
        if self.model.is_hint():
            return
        if ModeButton.mode == Mode.ENTRY:
            self.toggle_entry(event.keysym)
        else:
            self.toggle_note(event.keysym)
        self.show_number_buttons()

    def highlight_matching_numbers(self):
        import time
        matching_cells = [cell for cell in CellController.all_cells()
                          if cell.model.value == self.model.value
                          and (cell.model.has_value() or cell.model.value_type == CellValueType.ENTRY)
                          and cell.model is not self.model]
        for cell in matching_cells:
            if not cell.model.in_conflict:
                cell.view.update_color(CellView._MATCHING_COLOR)

    def show_number_buttons(self):
        NumberButton.toggle_all_off()
        if self.model.is_entry():
            NumberButton.toggle_entry_on(self.model.value)
        else:
            NumberButton.toggle_draft_on(self.model.notes)

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
    def clear_selected(cls, event):
        if cls.selected_cell.model.is_entry():
            cls.selected_cell.model.clear_entry()
            cls.selected_cell.view.update_color(False)
            cls.selected_cell.update_house_conflict_status()
        else:
            cls.selected_cell.model.clear_notes()

    @classmethod
    def toggle_selected_cell(cls, number):
        if cls.selected_cell is not None and not cls.selected_cell.model.is_given():
            if ModeButton.mode == Mode.ENTRY:
                cls.selected_cell.toggle_entry(number)
                cls.selected_cell.on_press(None)
            else:
                cls.selected_cell.toggle_note(number)

    def toggle_entry(self, keysym):
        self.model.set_entry(int(keysym))
        self.view.set_entry(int(keysym))
