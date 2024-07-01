from models.board_model import BoardModel
from observers.observer import Observer
from timer import Timer


class BoardStartObserver(Observer):
    """ Observers the board model, waiting for the user to select the first cell which determines the game start. """
    def __init__(self, board_model: BoardModel, timer: Timer):
        self.timer = timer
        self.board_model = board_model
        self.board_model.attach(self)
        self.game_has_started = False

    def update(self):
        """ Only updates once per game, once the first cell is selected. This starts the game timer. """
        if not self.game_has_started and self.board_model.is_any_cell_selected():
            self.game_has_started = True
            self.timer.start()
