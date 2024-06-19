from toggle_button import ToggleButton


class NumberButton(ToggleButton):
    buttons = {}
    __selected_button = None

    @classmethod
    def toggle_all_off(cls):
        [button.toggle_off() for button in cls.buttons.values()]

    @classmethod
    def toggle_entry_on(cls, number):
        if number:
            # print(type(number), number)
            cls.buttons[number].toggle_on()

    @classmethod
    def toggle_note_on(cls, notes):
        for i, should_toggle_on in enumerate(notes):
            if should_toggle_on:
                cls.buttons[i + 1].toggle_on()

    def __init__(self, parent, board_controller, number, **kwargs):
        super().__init__(parent, number, **kwargs)
        NumberButton.buttons[int(number)] = self
        self.board_controller = board_controller
        self.number = number

    def on_press(self, event):
        if NumberButton.__selected_button is not None and ModeButton.mode == Mode.ENTRY:
            NumberButton.__selected_button.toggle_off()
        NumberButton.__selected_button = self
        super().on_press(self)

        self.board_controller.toggle_selected_cell(self.number)

    @classmethod
    def show_number_buttons(cls, cell_controller):
        cls.toggle_all_off()
        if ModeButton.mode == Mode.ENTRY:
            cls.toggle_entry_on(cell_controller.model.value)
        elif ModeButton.mode == Mode.NOTES:
            cls.toggle_note_on(cell_controller.model.notes)


