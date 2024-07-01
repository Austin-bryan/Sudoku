from views.action_button import BUTTON_DEFAULT_COLOR
from views.toggle_button import ToggleButton


class NumberButton(ToggleButton):
    buttons = {}
    _selected_button = None
    _DISABLED_FILL = '#222'
    _DISABLED_TEXT = '#444'
    _DEFAULT_TEXT = '#FFF'
    _WIDTH = 100
    board_controller = None

    def __init__(self, parent, board_controller, number, **kwargs):
        super().__init__(parent, number, font_size=18, width=NumberButton._WIDTH, height=NumberButton._WIDTH, **kwargs)
        NumberButton.buttons[number] = self
        NumberButton.board_controller = board_controller
        self.number = number
        self._is_disabled = True
        self.disable()

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

    def on_press(self, event):
        """ Depending on the mode, toggles entries or notes, if it's enabled. """
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
        """ Turns appearance dark and makes sure it cant be interacted with. """
        self._is_disabled = True
        self._is_toggled = False
        self._set_color(NumberButton._DISABLED_FILL)
        self.itemconfig(self.text, fill=NumberButton._DISABLED_TEXT)

    def enable(self):
        """ Restores appearance and allows interaction. """
        self._is_disabled = False
        self._set_color(BUTTON_DEFAULT_COLOR)
        self.itemconfig(self.text, fill=NumberButton._DEFAULT_TEXT)

    @classmethod
    def show_number_buttons(cls, cell_controller):
        """
        Refreshes all number buttons.

        They are disabled if the selected cell is given, as it can't be changed.
        Shows the selected entry button if in entry mode and selecting an entry
        Shows all active notes if in note mode and selecting a cell with one or more notes.
        """
        cls.toggle_all_off()
        from views.mode_button import ModeButton, Mode

        if cell_controller.model.is_given() or not NumberButton.board_controller.model.is_any_cell_selected():
            cls.disable_all()
        else:
            cls.enable_all()
            if ModeButton.mode == Mode.ENTRY:
                cls.toggle_entry_on(cell_controller.model.value)
            elif ModeButton.mode == Mode.NOTES:
                cls.toggle_note_on(cell_controller.model.notes)
