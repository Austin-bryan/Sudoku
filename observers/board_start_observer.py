from observers.observer import Observer
from views.number_button import NumberButton


class BoardStartObserver(Observer):
    def __init__(self, board_model, timer):
        self.timer = timer
        self.board_model = board_model
        self.board_model.attach(self)
        self.first_cell_selected = False

    def update(self):
        if not self.first_cell_selected and self.board_model.is_any_cell_selected():
            # NumberButton.enable_all()
            self.first_cell_selected = True
            self.timer.start()
            print('hello')
