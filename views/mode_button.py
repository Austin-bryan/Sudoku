from tkinter import Frame, Tk
from enum import Enum
from typing import Union

from views.number_button import NumberButton
from views.toggle_button import ToggleButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.board_controller import BoardController  # pragma: no cover


class Mode(Enum):
    ENTRY = 0  # These take up the whole cell and can be in conflict
    NOTES = 1  # There are 9 notes, and they can't be in conflict.


class ModeButton(ToggleButton):
    """ Controls the mode of entering numbers between note mode or entry mode. """
    mode = Mode.ENTRY

    def __init__(self, parent: Union[Tk, Frame], board_controller: 'BoardController', label: str, **kwargs):
        super().__init__(parent, label, image_path='notes.png', **kwargs)
        self.board_controller = board_controller

    def on_press(self, event):
        """ Changes mode and updates number buttons to reflect that. """
        ModeButton.mode = Mode.NOTES if self.mode == Mode.ENTRY else Mode.ENTRY

        # Update number buttons to show the cells notes or entry
        # This will show the hidden cached notes, if in note mode but there is an entry in the cell,
        # Provided the cell has cached notes to begin with
        if self.board_controller.selected_cell:
            NumberButton.show_number_buttons(self.board_controller.selected_cell)

        super().on_press(self)
