from views.action_button import BUTTON_DEFAULT_COLOR
from views.toggle_button import ToggleButton
from tkinter import Frame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.board_controller import BoardController


class NumberButton(ToggleButton):
    """
    Allows the user to push buttons to enter numbers in cells.
    They can also use they keyboard for this purpose, but having buttons is standard.
    """
    buttons = {}
    _selected_button = None
    DISABLED_FILL = '#222'
    DISABLED_TEXT = '#444'
    DEFAULT_TEXT = '#FFF'
    WIDTH = 100
    board_controller = None

    def __init__(self, parent: Frame, board_controller: 'BoardController', number: int, **kwargs):
        super().__init__(parent, str(number), font_size=18,
                         width=NumberButton.WIDTH, height=NumberButton.WIDTH, **kwargs)
        NumberButton.buttons[number] = self
        NumberButton.board_controller = board_controller
        self.number = number
        self._is_disabled = True
        self.disable()

    @classmethod
    def toggle_all_off(cls):
        """ Turns off all buttons. """
        for button in cls.buttons.values():
            button.toggle_off()

    @classmethod
    def disable_all(cls):
        """ Disables all buttons. """
        for button in cls.buttons.values():
            button.disable()

    @classmethod
    def enable_all(cls):
        """ Enables all buttons. """
        for button in cls.buttons.values():
            button.enable()

    @classmethod
    def toggle_entry_on(cls, number: int):
        """
        Toggles the button on a given number.
        :param number: The number of the button to toggle.
        """
        if 0 <= number < len(cls.buttons):
            cls.buttons[number].toggle_on()

    @classmethod
    def toggle_note_on(cls, notes: list[int]):
        """
        Toggles on all notes from a cell.
        :param notes: The notes to toggle.
        """
        for i, should_toggle_on in enumerate(notes):
            if should_toggle_on:
                cls.buttons[i + 1].toggle_on()

    def on_press(self, event):
        """ Depending on the mode, toggles entries or notes, if it's enabled. """
        if self._is_disabled:
            return
        from views.mode_button import ModeButton, Mode

        # If in entry mode, turn off the currently selected button.
        if NumberButton._selected_button is not None and ModeButton.mode == Mode.ENTRY:
            NumberButton._selected_button.toggle_off()
        NumberButton._selected_button = self
        super().on_press(self)

        self.board_controller.toggle_selected_cell(self.number)

    def on_enter(self, event):
        """ Hover if not disabled. """
        if not self._is_disabled:
            super().on_enter(event)

    def on_leave(self, event):
        """ Return to default, if not disabled. """
        if not self._is_disabled:
            super().on_leave(event)

    def disable(self):
        """ Turns appearance dark and makes sure it cant be interacted with. """
        self._is_disabled = True
        self._is_toggled = False
        self._set_color(NumberButton.DISABLED_FILL)
        self.itemconfig(self.text, fill=NumberButton.DISABLED_TEXT)

    def enable(self):
        """ Restores appearance and allows interaction. """
        self._is_disabled = False
        self._set_color(BUTTON_DEFAULT_COLOR)
        self.itemconfig(self.text, fill=NumberButton.DEFAULT_TEXT)

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

        if cell_controller.model.is_given() or not NumberButton.board_controller.model.is_any_cell_selected() or \
                not NumberButton.board_controller.can_select:
            cls.disable_all()
        else:
            cls.enable_all()
            if ModeButton.mode == Mode.ENTRY:
                cls.toggle_entry_on(cell_controller.model.value)
            elif ModeButton.mode == Mode.NOTES:
                cls.toggle_note_on(cell_controller.model.notes)
