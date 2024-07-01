from models.board_model import BoardModel
from models.subject import Subject
from observers.observer import Observer


class IsSolvedObserver(Observer, Subject):
    """ Observes the board model, detecting when the game is solved. """
    def __init__(self, board_model: BoardModel):
        super().__init__()
        self.board_model = board_model
        self.board_model.attach(self)

    def update(self):
        """ Notify observers when it detects the board model is solved. """
        if self.is_solved():
            self.notify()

    def is_solved(self):
        """
        If all cells are both
            A) Not None and
            B) Not in conflict
        Then the game is solved.
        """
        for row in self.board_model.cells:
            for cell in row:
                if cell.value is None:
                    return False
                if cell.in_conflict:
                    return False
        return True
