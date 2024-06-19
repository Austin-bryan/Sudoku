from enum import Enum
from number_button import NumberButton
from toggle_button import ToggleButton


class Mode(Enum):
    ENTRY = 0
    NOTES = 1


class ModeButton(ToggleButton):
    mode = Mode.ENTRY

    def __init__(self, parent, board_controller, label, **kwargs):
        super().__init__(parent, label, **kwargs)
        self.board_controller = board_controller

    def on_press(self, event):
        ModeButton.mode = Mode.NOTES if self.mode == Mode.ENTRY else Mode.ENTRY

        if self.board_controller.selected_cell:
            NumberButton.show_number_buttons(self.board_controller.selected_cell)

        super().on_press(self)
