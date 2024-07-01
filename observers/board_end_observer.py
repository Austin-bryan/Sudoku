from observers.observer import Observer
from views.number_button import NumberButton
import time


class BoardEndObserver(Observer):
    def __init__(self, is_solved_observer, timer, board_controller, board_start):
        self.timer = timer
        self.is_solved_observer = is_solved_observer
        self.is_solved_observer.attach(self)
        self.board_controller = board_controller
        self.board_start = board_start

    def update(self):
        self.board_controller.return_to_default()
        self.board_controller.can_select = False
        self.timer.stop()
        NumberButton.disable_all()
