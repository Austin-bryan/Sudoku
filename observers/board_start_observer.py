from observers.observer import Observer


class BoardStartObserver(Observer):
    def __init__(self, board_model, timer):
        self.timer = timer
        self.board_model = board_model
        self.board_model.attach(self)
        self.first_cell_selected = False

    def update(self):
        if not self.first_cell_selected and self.board_model.is_any_cell_selected():
            print('update 2')
            self.first_cell_selected = True
            self.timer.start()
