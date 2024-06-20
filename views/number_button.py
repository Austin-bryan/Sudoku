from views.toggle_button import ToggleButton


class NumberButton(ToggleButton):
    buttons = {}
    _selected_button = None
    _DISABLED_FILL = '#222'
    _DISABLED_TEXT = '#444'
    _DEFAULT_TEXT = '#FFF'

    @classmethod
    def toggle_all_off(cls):
        [button.toggle_off() for button in cls.buttons.values()]

    @classmethod
    def disable_all(cls):
        [button.disable() for button in cls.buttons.values()]

    @classmethod
    def enable_all(cls):
        [button.enable() for button in cls.buttons.values()]

    @classmethod
    def toggle_entry_on(cls, number):
        if number:
            cls.buttons[number].toggle_on()

    @classmethod
    def toggle_note_on(cls, notes):
        for i, should_toggle_on in enumerate(notes):
            if should_toggle_on:
                cls.buttons[i + 1].toggle_on()

    def __init__(self, parent, board_controller, number, **kwargs):
        super().__init__(parent, number, **kwargs)
        NumberButton.buttons[number] = self
        self.board_controller = board_controller
        self.number = number
        self._is_disabled = True
        self.disable()

    def on_press(self, event):
        if self._is_disabled:
            return
        from views.mode_button import ModeButton, Mode
        if NumberButton._selected_button is not None and ModeButton.mode == Mode.ENTRY:
            NumberButton._selected_button.toggle_off()
        NumberButton._selected_button = self
        super().on_press(self)

        self.board_controller.toggle_selected_cell(self.number)

    def on_enter(self, event):
        if not self._is_disabled:
            super().on_enter(event)

    def on_leave(self, event):
        if not self._is_disabled:
            super().on_leave(event)

    def disable(self):
        self._is_disabled = True
        self._is_toggled = False
        self._set_color(NumberButton._DISABLED_FILL)
        self.itemconfig(self.text, fill=NumberButton._DISABLED_TEXT)

    def enable(self):
        self._is_disabled = False
        self._set_color(ToggleButton._DEFAULT_COLOR)
        self.itemconfig(self.text, fill=NumberButton._DEFAULT_TEXT)

    @classmethod
    def show_number_buttons(cls, cell_controller):
        cls.toggle_all_off()
        from views.mode_button import ModeButton, Mode

        if cell_controller.model.is_given():
            cls.disable_all()
        else:
            cls.enable_all()
            if ModeButton.mode == Mode.ENTRY:
                cls.toggle_entry_on(cell_controller.model.value)
            elif ModeButton.mode == Mode.NOTES:
                cls.toggle_note_on(cell_controller.model.notes)
