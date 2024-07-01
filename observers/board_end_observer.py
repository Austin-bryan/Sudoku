from controllers.board_controller import BoardController
from observers.board_start_observer import BoardStartObserver
from observers.is_solved_observer import IsSolvedObserver
from observers.observer import Observer
from timer import Timer
from views.number_button import NumberButton


class BoardEndObserver(Observer):
    """ Observers the IsSolvedObserver, to know when the game has been beaten so we can do game clear stuff. """
    def __init__(self, is_solved_observer: IsSolvedObserver, timer: Timer, board_controller: BoardController,
                 board_start: BoardStartObserver):
        self.timer = timer
        self.is_solved_observer = is_solved_observer
        self.is_solved_observer.attach(self)
        self.board_controller = board_controller
        self.board_start = board_start

    def update(self):
        """ Does a few end game stuff to finish this game and setup for the next game. """
        self.board_controller.return_to_default()
        self.board_controller.can_select = False
        self.timer.stop()
        NumberButton.disable_all()
