from models.subject import Subject
from observers.observer import Observer
from views.number_button import NumberButton


class IsSolvedObserver(Observer, Subject):
    def __init__(self, board_model):
        super().__init__()
        self.board_model = board_model
        self.board_model.attach(self)

    def update(self):
        if self.is_solved():
            self.notify()

    def is_solved(self):
        for row in self.board_model.cells:
            for cell in row:
                if cell.value is None:
                    return False
                if cell.in_conflict:
                    return False
        return True
