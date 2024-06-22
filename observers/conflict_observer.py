from observers.observer import Observer
from utils.constants import BOARD_SIZE


class ConflictObserver(Observer):
    def __init__(self, board_model):
        self.board_model = board_model
        self.board_model.attach(self)

    def update(self):
        self.detect_conflicts()

    def detect_conflicts(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                cell_model = self.board_model.get_cell(x, y)
                cell_model.set_conflict_status(self.has_conflict(cell_model))

    def has_conflict(self, cell_model):
        return self.has_duplicates(cell_model, cell_model.get_house())

    @staticmethod
    def has_duplicates(cell_model, house):
        values = [cell.value for cell in house if cell.value != 0 and cell.value is not None]
        for value in values:
            if value == cell_model.value:
                return True
        return False
