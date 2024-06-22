from utils.constants import BOARD_SIZE


class ConflictObserver:
    def __init__(self, board_model):
        self.board_model = board_model
        self.board_model.attach(self)

    def update(self):
        self.detect_conflicts()

    def detect_conflicts(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                cell_controller = self.board_model.get_cell(x, y)
                cell_controller.set_conflict_status(self.has_conflict(cell_controller))

    def has_conflict(self, cell_controller):
        return self.has_duplicates(cell_controller.get_house())

    @staticmethod
    def has_duplicates(values):
        nums = [v for v in values if v != 0]
        return len(nums) != len(set(nums))
